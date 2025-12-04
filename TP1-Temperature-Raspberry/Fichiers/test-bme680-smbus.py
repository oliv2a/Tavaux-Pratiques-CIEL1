#!/usr/bin/env python3
"""
Test du capteur BME680 avec smbus
Affiche la température et l'humidité
"""

import smbus2
import time

# Adresse I2C du BME680 (0x76 ou 0x77 selon le modèle)
BME680_ADDR = 0x77

# Registres BME680
REG_CHIP_ID = 0xD0
REG_RESET = 0xE0
REG_CTRL_HUM = 0x72
REG_CTRL_MEAS = 0x74
REG_CONFIG = 0x75

# Registres de données
REG_TEMP_MSB = 0x22
REG_HUM_MSB = 0x25

# Chip ID attendu
CHIP_ID_BME680 = 0x61

class BME680:
    def __init__(self, bus_number=1, address=BME680_ADDR):
        """Initialise le capteur BME680"""
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        
        # Vérifier le chip ID
        chip_id = self.bus.read_byte_data(self.address, REG_CHIP_ID)
        if chip_id != CHIP_ID_BME680:
            raise Exception(f"BME680 non détecté! Chip ID: 0x{chip_id:02X} (attendu: 0x{CHIP_ID_BME680:02X})")
        
        print(f"BME680 détecté (Chip ID: 0x{chip_id:02X})")
        
        # Lire les coefficients de calibration
        self._read_calibration_data()
        
        # Configurer le capteur
        self._configure()
    
    def _read_calibration_data(self):
        """Lit les coefficients de calibration depuis le capteur"""
        # Température
        coeff = self.bus.read_i2c_block_data(self.address, 0x89, 3)
        self.par_t1 = (coeff[1] << 8) | coeff[0]
        self.par_t2 = (coeff[2] << 8) | coeff[1]
        
        coeff = self.bus.read_byte_data(self.address, 0x8A)
        self.par_t3 = coeff
        
        # Humidité
        coeff = self.bus.read_i2c_block_data(self.address, 0xE1, 7)
        self.par_h1 = (coeff[2] << 4) | (coeff[1] & 0x0F)
        self.par_h2 = (coeff[0] << 4) | (coeff[1] >> 4)
        self.par_h3 = coeff[3]
        self.par_h4 = coeff[4]
        self.par_h5 = coeff[5]
        self.par_h6 = coeff[6]
        
        coeff = self.bus.read_byte_data(self.address, 0xE7)
        self.par_h7 = coeff
        
        print("Coefficients de calibration chargés")
    
    def _configure(self):
        """Configure le capteur pour les mesures"""
        # Configurer l'humidité (oversampling x2)
        self.bus.write_byte_data(self.address, REG_CTRL_HUM, 0x02)
        
        # Configurer température et pression (oversampling x2, mode forcé)
        # Mode forcé: le capteur fait une mesure puis retourne en veille
        self.bus.write_byte_data(self.address, REG_CTRL_MEAS, 0x49)
        
        # Configurer le filtre IIR (coefficient 3)
        self.bus.write_byte_data(self.address, REG_CONFIG, 0x0C)
        
        print("Capteur configuré")
    
    def _read_raw_data(self):
        """Lit les données brutes du capteur"""
        # Déclencher une mesure (mode forcé)
        self.bus.write_byte_data(self.address, REG_CTRL_MEAS, 0x49)
        
        # Attendre la fin de la mesure
        time.sleep(0.5)
        
        # Lire les données de température (3 octets)
        data = self.bus.read_i2c_block_data(self.address, REG_TEMP_MSB, 3)
        adc_temp = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        
        # Lire les données d'humidité (2 octets)
        data = self.bus.read_i2c_block_data(self.address, REG_HUM_MSB, 2)
        adc_hum = (data[0] << 8) | data[1]
        
        return adc_temp, adc_hum
    
    def _compensate_temperature(self, adc_temp):
        """Compense la température avec les coefficients de calibration"""
        var1 = (adc_temp >> 3) - (self.par_t1 << 1)
        var2 = (var1 * self.par_t2) >> 11
        var3 = ((var1 >> 1) * (var1 >> 1)) >> 12
        var3 = ((var3) * (self.par_t3 << 4)) >> 14
        
        self.t_fine = var2 + var3
        calc_temp = (((self.t_fine * 5) + 128) >> 8)
        
        return calc_temp / 100.0
    
    def _compensate_humidity(self, adc_hum):
        """Compense l'humidité avec les coefficients de calibration"""
        temp_scaled = ((self.t_fine * 5) + 128) >> 8
        var1 = (adc_hum - ((self.par_h1 * 16))) - (((temp_scaled * self.par_h3) // 100) >> 1)
        var2 = (self.par_h2 * (((temp_scaled * self.par_h4) // 100) + 
                (((temp_scaled * ((temp_scaled * self.par_h5) // 100)) >> 6) // 100) + 
                (1 << 14))) >> 10
        var3 = var1 * var2
        var4 = self.par_h6 << 7
        var4 = ((var4) + ((temp_scaled * self.par_h7) // 100)) >> 4
        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1
        calc_hum = (((var3 + var6) >> 10) * 1000) >> 12
        
        # Limiter entre 0% et 100%
        calc_hum = max(0, min(100000, calc_hum))
        
        return calc_hum / 1000.0
    
    def read(self):
        """Lit température et humidité"""
        adc_temp, adc_hum = self._read_raw_data()
        
        temperature = self._compensate_temperature(adc_temp)
        humidity = self._compensate_humidity(adc_hum)
        
        return temperature, humidity


def main():
    """Fonction principale"""
    print("=== Test du capteur BME680 ===\n")
    
    try:
        # Initialiser le capteur
        sensor = BME680()
        print("\nDémarrage des mesures...\n")
        
        # Boucle de mesure
        while True:
            # Lire les valeurs
            temperature, humidity = sensor.read()
            
            # Afficher les résultats
            print(f"Température: {temperature:6.2f}°C | Humidité: {humidity:6.2f}%")
            
            # Attendre 2 secondes avant la prochaine mesure
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nArrêt du programme")
    except Exception as e:
        print(f"\nErreur: {e}")
        print("\nVérifiez:")
        print("  - Le câblage du capteur")
        print("  - L'adresse I2C (0x76 ou 0x77)")
        print("  - Que l'I2C est activé: sudo raspi-config")


if __name__ == "__main__":
    main()
