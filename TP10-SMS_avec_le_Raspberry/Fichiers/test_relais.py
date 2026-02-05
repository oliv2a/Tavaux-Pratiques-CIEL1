#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAIS_1 = 17
RELAIS_2 = 27

# Initialisation des GPIO en sortie
GPIO.setup(RELAIS_1, GPIO.OUT)
GPIO.setup(RELAIS_2, GPIO.OUT)

# État initial : relais ouverts (électrovannes OFF)
GPIO.output(RELAIS_1, GPIO.HIGH)
GPIO.output(RELAIS_2, GPIO.HIGH)

print("Test des relais")
print("=" * 40)

try:
    print("Activation Relais 1 (3 secondes)...")
    GPIO.output(RELAIS_1, GPIO.LOW)  # Fermer relais
    time.sleep(3)
    GPIO.output(RELAIS_1, GPIO.HIGH)  # Ouvrir relais
    print("✓ Relais 1 OK\n")
    
    time.sleep(1)
    
    print("Activation Relais 2 (3 secondes)...")
    GPIO.output(RELAIS_2, GPIO.LOW)
    time.sleep(3)
    GPIO.output(RELAIS_2, GPIO.HIGH)
    print("✓ Relais 2 OK\n")
    
    print("✅ Test terminé")

except KeyboardInterrupt:
    print("\nInterrompu")

finally:
    GPIO.cleanup()