import subprocess
import re
import time
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Function to scan Wi-Fi networks
def scan_wifi():
    networks = []
    
    # Run the command to scan for networks depending on the OS
    try:
        # For Linux
        command = "sudo iwlist scan"  # Use iwlist scan on Linux
        scan_results = subprocess.check_output(command, shell=True).decode()

        # Regex to extract network information
        networks = re.findall(r"Cell \d+ - Address: (\S+).*?ESSID:\"([^\"]+)\".*?Signal level=(-?\d+)", scan_results, re.DOTALL)
    
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error scanning Wi-Fi networks. Please check your Wi-Fi adapter and permissions.")
    
    return networks

# Function to display Wi-Fi networks
def display_wifi(networks):
    print(f"{Fore.YELLOW}Wi-Fi Networks Found:\n")
    for idx, (mac, ssid, signal) in enumerate(networks):
        print(f"{Fore.GREEN}[{idx+1}] {Fore.CYAN}SSID:{Fore.WHITE} {ssid}, {Fore.CYAN}MAC:{Fore.WHITE} {mac}, {Fore.CYAN}Signal:{Fore.WHITE} {signal}dBm")

# Main function to run the Wi-Fi scanner
def main():
    print(f"{Fore.GREEN}Starting Wi-Fi Scanner...")

    time.sleep(2)
    print(f"{Fore.CYAN}Scanning for available Wi-Fi networks...\n")
    
    # Scan for Wi-Fi networks
    networks = scan_wifi()

    if networks:
        display_wifi(networks)
    else:
        print(f"{Fore.RED}No Wi-Fi networks found or failed to scan.")

if __name__ == "__main__":
    main()
