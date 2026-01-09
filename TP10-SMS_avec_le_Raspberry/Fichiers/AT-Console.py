import serial
import time

# Liste des baudrates possibles
baudrates = [9600, 19200, 38400, 57600, 115200]

print("=== Terminal AT ===")
print("Sélectionnez le baudrate :")
for i, br in enumerate(baudrates, start=1):
    print(f"{i}. {br}")

choix = input("Votre choix (1-5) : ")

try:
    baudrate = baudrates[int(choix) - 1]
except (ValueError, IndexError):
    print("Choix invalide, baudrate par défaut : 9600")
    baudrate = 9600

# Configuration du port série
ser = serial.Serial(
    port='/dev/serial0',  # ou '/dev/ttyAMA0' / '/dev/ttyS0'
    baudrate=baudrate,
    timeout=1
)

print(f"\nPort ouvert à {baudrate} bauds")
print("Tapez une commande AT (ex: AT, AT+BTSCAN).")
print("Tapez 'quit' pour sortir.\n")

try:
    while True:
        # Lecture de la commande saisie au clavier
        cmd = input(">>> ")
        if cmd.lower() == "quit":
            break

        # Envoi avec CR+LF
        ser.write((cmd + "\r\n").encode("utf-8"))

        # Pause pour laisser la réponse arriver
        time.sleep(0.2)

        # Lecture des réponses disponibles
        while ser.in_waiting > 0:
            ligne = ser.readline().decode("utf-8", errors="ignore").strip()
            if ligne:
                print(f"<<< {ligne}")

except KeyboardInterrupt:
    print("\nArrêt du programme.")

finally:
    ser.close()
    print("Port série fermé.")
