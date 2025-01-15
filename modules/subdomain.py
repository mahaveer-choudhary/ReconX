import requests
import threading
import queue
from colorama import Fore, init
import sys

init(autoreset=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# virustotal_api_key = 9130c6dcf28a940b2cf763edd3b2cb964b6ccedaab832f9beecd21f57eb605ea

def query_api_hackertarget(domain):
    """Query HackerTarget API for subdomains"""
    print(f"{Fore.CYAN}[INFO] Querying HackerTarget for subdomains...")
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return [line.split(",")[0] for line in response.text.splitlines()]
        else:
            print(f"{Fore.RED}[ERROR] HackerTarget API failed. Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to query HackerTarget: {e}")
        return []


def query_api_virustotal(domain, api_key):
    """Query VirusTotal API for subdomains"""
    print(f"{Fore.CYAN}[INFO] Querying VirusTotal for subdomains...")
    url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [item["id"] for item in data.get("data", [])]
        else:
            print(f"{Fore.RED}[ERROR] VirusTotal API failed. Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to query VirusTotal: {e}")
        return []


def brute_force_subdomains(domain, wordlist):
    """Brute force subdomains using a wordlist"""
    print(f"{Fore.CYAN}[INFO] Performing brute force enumeration...")
    subdomains = []
    q = queue.Queue()

    def worker():
        while not q.empty():
            subdomain = q.get()
            url = f"http://{subdomain}.{domain}"
            try:
                response = requests.get(url, headers=HEADERS, timeout=5)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[FOUND] {url}")
                    subdomains.append(url)
            except requests.exceptions.RequestException:
                pass
            q.task_done()

    # Load wordlist into queue
    with open(wordlist, "r") as f:
        for line in f:
            q.put(line.strip())

    # Create threads
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    q.join()
    for t in threads:
        t.join()

    return subdomains


def main():
    print(f"{Fore.GREEN}[INFO] Subdomain Enumeration Tool")
    print(f"{Fore.LIGHTMAGENTA_EX}By Mahaveer\n")

    domain = input(f"{Fore.BLUE}Enter the domain to enumerate: {Fore.RESET}").strip()
    api_key = input(f"{Fore.BLUE}Enter your VirusTotal API Key (leave blank to skip): {Fore.RESET}").strip()
    wordlist = input(f"{Fore.BLUE}Enter the path to your wordlist for brute force (leave blank to skip): {Fore.RESET}").strip()

    subdomains = set()

    # Query APIs
    subdomains.update(query_api_hackertarget(domain))
    if api_key:
        subdomains.update(query_api_virustotal(domain, api_key))

    # Perform brute force
    if wordlist:
        subdomains.update(brute_force_subdomains(domain, wordlist))

    # Display results
    if subdomains:
        print(f"{Fore.GREEN}[INFO] Subdomains found:")
        for subdomain in sorted(subdomains):
            print(f"  - {subdomain}")
    else:
        print(f"{Fore.RED}[INFO] No subdomains found.")

    # Save results to a file
    output_file = input(f"{Fore.BLUE}Enter output file name to save results (leave blank to skip): {Fore.RESET}").strip()
    if output_file:
        with open(output_file, "w") as f:
            for subdomain in sorted(subdomains):
                f.write(subdomain + "\n")
        print(f"{Fore.GREEN}[INFO] Results saved to {output_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[INFO] Exiting...")
        sys.exit(0)
