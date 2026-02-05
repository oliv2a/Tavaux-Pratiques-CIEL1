#!/usr/bin/env python3
import serial
import time
import sys
import termios
import tty

# Configuration du port série
PORT = "/dev/ttyS0"
BAUDRATE = 115200

class ATConsole:
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            print(f"✓ Connecté à {port} à {baudrate} baud")
            print("=" * 50)
            print("Console AT pour SIM800C")
            print("Tapez vos commandes AT (Ctrl+C pour quitter)")
            print("Pour envoyer un SMS : utilisez F10 au lieu de Ctrl+Z")
            print("=" * 50)
        except Exception as e:
            print(f"✗ Erreur de connexion : {e}")
            sys.exit(1)
    
    def send_command(self, command):
        """Envoie une commande AT et affiche la réponse"""
        try:
            # Envoi de la commande
            self.ser.write((command + '\r').encode())
            time.sleep(0.5)
            
            # Lecture de la réponse
            response = ""
            while self.ser.in_waiting:
                response += self.ser.read(self.ser.in_waiting).decode(errors='ignore')
                time.sleep(0.1)
            
            return response
        except Exception as e:
            return f"Erreur : {e}"
    
    def read_multiline_input(self):
        """Lecture en mode multiligne pour les SMS"""
        print("Mode SMS activé. Tapez votre message.")
        print("Appuyez sur F10 pour envoyer (Ctrl+Z)")
        print("-" * 50)
        
        # Sauvegarde des paramètres du terminal
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            # Mode raw pour capturer F10
            tty.setraw(sys.stdin.fileno())
            
            message = ""
            
            while True:
                char = sys.stdin.read(1)
                
                # Détection de F10 : séquence ESC[21~
                if char == '\x1b':  # ESC
                    seq = sys.stdin.read(2)
                    if seq == '[2':
                        next_char = sys.stdin.read(1)
                        if next_char == '1':
                            final = sys.stdin.read(1)
                            if final == '~':
                                # F10 détecté, envoyer Ctrl+Z
                                sys.stdout.write('\n')
                                sys.stdout.flush()
                                return message + '\x1A'  # Ajout du Ctrl+Z
                
                # Ctrl+C pour annuler
                elif char == '\x03':
                    raise KeyboardInterrupt
                
                # Backspace
                elif char == '\x7f':
                    if message:
                        message = message[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                
                # Entrée
                elif char == '\r' or char == '\n':
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    message += '\n'
                
                # Caractère normal
                elif ord(char) >= 32:
                    message += char
                    sys.stdout.write(char)
                    sys.stdout.flush()
        
        finally:
            # Restauration des paramètres du terminal
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    def run(self):
        """Boucle principale de la console"""
        while True:
            try:
                # Lecture de la commande utilisateur
                cmd = input("AT> ")
                
                if not cmd:
                    continue
                
                # Détection du mode SMS
                if cmd.upper().startswith("AT+CMGS"):
                    # Envoi de la commande AT+CMGS
                    response = self.send_command(cmd)
                    print(response)
                    
                    # Si le module répond avec >, passer en mode saisie SMS
                    if '>' in response:
                        # Lecture du message en mode multiligne
                        message = self.read_multiline_input()
                        
                        # Envoi du message
                        self.ser.write(message.encode())
                        time.sleep(5)  # Attendre l'envoi
                        
                        # Lecture de la réponse
                        response = ""
                        while self.ser.in_waiting:
                            response += self.ser.read(self.ser.in_waiting).decode(errors='ignore')
                            time.sleep(0.1)
                        
                        print(response)
                else:
                    # Commande AT normale
                    response = self.send_command(cmd)
                    print(response)
                
            except KeyboardInterrupt:
                print("\n\n✓ Fermeture de la console")
                self.ser.close()
                break
            except Exception as e:
                print(f"Erreur : {e}")

if __name__ == "__main__":
    console = ATConsole(PORT, BAUDRATE)
    console.run()