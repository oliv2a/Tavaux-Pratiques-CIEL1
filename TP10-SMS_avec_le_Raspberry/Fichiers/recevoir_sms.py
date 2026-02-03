import serial
import time

port = "/dev/ttyS0"
baudrate = 115200

def lire_sms():
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        
        # Mode texte
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
        # Paramétrage pour afficher les détails
        ser.write(b'AT+CSDH=1\r')
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
        # Lire tous les SMS
        print("Lecture des SMS...\n")
        ser.write(b'AT+CMGL="ALL"\r')
        time.sleep(2)
        
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        print(reponse)
        
        ser.close()
        
    except Exception as e:
        print(f"Erreur : {e}")

lire_sms()