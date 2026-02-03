import serial
import time

# Configuration du port série
port = "/dev/ttyS0"
baudrate = 115200

def envoyer_sms(numero, message):
    try:
        # Connexion au module SIM800C
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        
        print("Test de communication...")
        ser.write(b'AT\r')
        time.sleep(0.5)
        print(ser.read(ser.in_waiting).decode())
        
        # Mode texte pour les SMS
        print("Configuration mode texte...")
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        print(ser.read(ser.in_waiting).decode())
        
        # Envoi du numéro de destination
        print(f"Envoi vers {numero}...")
        ser.write(f'AT+CMGS="{numero}"\r'.encode())
        time.sleep(0.5)
        print(ser.read(ser.in_waiting).decode())
        
        # Envoi du message (terminer par Ctrl+Z = caractère 26)
        ser.write(f'{message}\x1A'.encode())
        time.sleep(5)  # Attendre l'envoi
        reponse = ser.read(ser.in_waiting).decode()
        print(reponse)
        
        if "+CMGS:" in reponse:
            print("✓ SMS envoyé avec succès !")
        else:
            print("✗ Erreur lors de l'envoi")
        
        ser.close()
        
    except Exception as e:
        print(f"Erreur : {e}")

# Test
numero_destination = "+33612345678"  # Remplace par ton numéro
message = "Test SMS depuis Raspberry Pi"

envoyer_sms(numero_destination, message)