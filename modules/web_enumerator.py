import requests
from bs4 import BeautifulSoup
import socket
import json
import threading
import subprocess
from queue import Queue
from colorama import Fore, init
import sys

# Initialize colorama
init(autoreset=True)

class WebServerEnumerator:
    def __init__(self, url, output_file="results.json"):
        self.url = url if url.startswith("http") else f"http://{url}"
        self.output_file = output_file
        self.results = {
            "url": self.url,
            "headers": {},
            "technologies": [],
            "default_pages": [],
            "os_guess": None
        }
        self.common_paths = [
            "/server-status", "/phpinfo.php", "/nginx_status", "/robots.txt",
            "/admin", "/login", "/wp-admin", "/.git"
        ]
        self.queue = Queue()

    def fetch_headers(self):
        try:
            response = requests.get(self.url, timeout=5)
            self.results["headers"] = dict(response.headers)
            print(Fore.GREEN + "[*] Fetched headers successfully.")
        except Exception as e:
            print(Fore.RED + f"[!] Error fetching headers: {e}")

    def analyze_content(self):
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            meta_tags = soup.find_all("meta")
            for tag in meta_tags:
                if "name" in tag.attrs or "content" in tag.attrs:
                    self.results["technologies"].append(tag.attrs)
            print(Fore.GREEN + "[*] Analyzed page content for technologies.")
        except Exception as e:
            print(Fore.RED + f"[!] Error analyzing content: {e}")

    def check_common_paths(self):
        def worker():
            while not self.queue.empty():
                path = self.queue.get()
                test_url = self.url.rstrip("/") + path
                try:
                    response = requests.get(test_url, timeout=5)
                    if response.status_code == 200:
                        self.results["default_pages"].append(test_url)
                        print(Fore.CYAN + f"[+] Found default page: {test_url}")
                except Exception:
                    pass
                finally:
                    self.queue.task_done()

        for path in self.common_paths:
            self.queue.put(path)

        for _ in range(5):
            t = threading.Thread(target=worker)
            t.start()

        self.queue.join()

    def infer_os(self):
        try:
            hostname = self.url.split("//")[-1].split("/")[0]
            ip_address = socket.gethostbyname(hostname)
            ttl = self.get_ttl(ip_address)
            if ttl:
                if ttl > 128:
                    self.results["os_guess"] = "Unix/Linux (likely)"
                elif ttl > 64:
                    self.results["os_guess"] = "Windows (likely)"
                else:
                    self.results["os_guess"] = "Unknown"
            print(Fore.GREEN + "[*] OS inference completed.")
        except Exception as e:
            print(Fore.RED + f"[!] Error inferring OS: {e}")

    def get_ttl(self, ip):
        try:
            process = subprocess.Popen(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()

            if "TTL=" in stdout:
                ttl_value = int(stdout.split("TTL=")[-1].split()[0])
                return ttl_value
        except Exception as e:
            print(Fore.RED + f"[!] Error getting TTL: {e}")
        return None

    def save_results(self):
        try:
            with open(self.output_file, "w") as file:
                json.dump(self.results, file, indent=4)
            print(Fore.GREEN + f"[*] Results saved to {self.output_file}.")
        except Exception as e:
            print(Fore.RED + f"[!] Error saving results: {e}")

    def display_results(self):
        print(Fore.MAGENTA + "\n[*] Web Server Enumeration Results:")
        print(Fore.YELLOW + f"\nURL: {self.results['url']}")

        print(Fore.YELLOW + "\n[*] HTTP Headers:")
        for key, value in self.results["headers"].items():
            print(Fore.CYAN + f"  {key}: {value}")

        print(Fore.YELLOW + "\n[*] Technologies Detected:")
        if self.results["technologies"]:
            for tech in self.results["technologies"]:
                print(Fore.CYAN + f"  {tech}")
        else:
            print(Fore.RED + "  No technologies detected.")

        print(Fore.YELLOW + "\n[*] Default Pages Found:")
        if self.results["default_pages"]:
            for page in self.results["default_pages"]:
                print(Fore.CYAN + f"  {page}")
        else:
            print(Fore.RED + "  No default pages found.")

        print(Fore.YELLOW + "\n[*] OS Guess:")
        if self.results["os_guess"]:
            print(Fore.CYAN + f"  {self.results['os_guess']}")
        else:
            print(Fore.RED + "  Unable to infer OS.")

    def run(self):
        print(Fore.GREEN + "[*] Starting Web Server Enumeration...")
        self.fetch_headers()
        self.analyze_content()
        self.check_common_paths()
        self.infer_os()
        self.display_results()

        save_option = input(Fore.GREEN + "\nDo you want to save the results to a file? (y/n): ").strip().lower()
        if save_option == 'y':
            self.save_results()

# Function for integrating into the framework
def run_web_server_enumeration(url):
    tool = WebServerEnumerator(url)
    tool.run()

# Standalone execution support
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python web_server_enumeration.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    run_web_server_enumeration(url)
