import argparse
import socket
import threading
from datetime import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Function to check if the port is open or closed
def scan_port(target, port, result, lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result[port] = 'Closed'

    try:
        sock.connect((target, port))
    except (socket.timeout, socket.error):
        pass
    else:
        result[port] = 'Open'
    finally:
        sock.close()

# Main function to scan a range of ports
def main(target, start_port, end_port, threads):
    print(f"{Fore.GREEN}Starting Service Scanner for {target} ({start_port}-{end_port})")
    print(f"{Fore.YELLOW}Scan started at: {datetime.now()}")

    result = {}
    lock = threading.Lock()
    threads_list = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port, result, lock))
        threads_list.append(thread)
        thread.start()

        # Limit number of threads (wait for completion if the number exceeds the max threads limit)
        if len(threads_list) >= threads:
            for t in threads_list:
                t.join()
            threads_list = []

    # Wait for remaining threads
    for t in threads_list:
        t.join()

    # Print results
    print(f"\n{Fore.YELLOW}Scan completed at:", datetime.now())
    print(f"{Fore.CYAN}Results:")
    for port, status in result.items():
        if status == 'Open':
            print(f"{Fore.GREEN}Port {port}: {status}")
        else:
            print(f"{Fore.RED}Port {port}: {status}")

# Check if the script is being run directly
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Service Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("--start-port", type=int, default=1, help="Start port number")
    parser.add_argument("--end-port", type=int, default=1024, help="End port number")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for scanning")

    # Parse arguments
    args = parser.parse_args()

    # Run the service scanner
    main(args.target, args.start_port, args.end_port, args.threads)
