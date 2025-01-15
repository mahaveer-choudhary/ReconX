import dns.resolver
import dns.zone
import dns.query
import json
from colorama import Fore, init

def dsnenum(domain, output=None, verbose=False):
    """DNS Enumeration Function"""
    def get_dns_records(domain, record_type):
        """Fetch DNS records for a specific type."""
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [rdata.to_text() for rdata in answers]
        except dns.resolver.NoAnswer:
            return []
        except Exception as e:
            return [f"Error: {e}"]

    def zone_transfer(domain):
        """Attempt zone transfer and return retrieved entries."""
        try:
            ns_records = get_dns_records(domain, "NS")
            for ns in ns_records:
                try:
                    print(f"{Fore.BLUE}Testing zone transfer on {Fore.YELLOW}{ns}{Fore.RESET}...")
                    zone = dns.zone.from_xfr(dns.query.xfr(ns, domain))
                    if zone:
                        return [str(name) for name in zone.nodes.keys()]
                except Exception:
                    continue
            return []
        except Exception as e:
            return [f"{Fore.RED}Error: {e}{Fore.RESET}"]

    def save_results_to_json(data, filename):
        """Save DNS records to a JSON file."""
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"{Fore.GREEN}Results saved to {filename}.{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error saving results: {e}{Fore.RESET}")

    # Main enumeration logic
    print(f"{Fore.GREEN}Enumerating DNS records for {Fore.BLUE}{domain}{Fore.RESET}...\n")

    results = {
        "A": get_dns_records(domain, "A"),
        "MX": get_dns_records(domain, "MX"),
        "NS": get_dns_records(domain, "NS"),
        "CNAME": get_dns_records(domain, "CNAME"),
        "TXT": get_dns_records(domain, "TXT"),
    }

    for record_type, data in results.items():
        if verbose or data:
            print(f"{Fore.YELLOW}{record_type} Records:{Fore.RESET}")
            for entry in data:
                print(f"  - {entry}")
            print()

    print(f"{Fore.GREEN}Checking for zone transfer...\n")
    zone_results = zone_transfer(domain)
    if zone_results:
        print(f"{Fore.BLUE}Zone transfer successful. Retrieved entries:{Fore.RESET}")
        for entry in zone_results:
            print(f"  - {entry}")
    else:
        print(f"{Fore.RED}Zone transfer not allowed.{Fore.RESET}")

    if output:
        save_results_to_json(results, output)

if __name__ == "__main__":
    import argparse

    # Initialize colorama
    init(autoreset=True)

    # Command-line arguments
    parser = argparse.ArgumentParser(description="Advanced DNS Enumeration Tool")
    parser.add_argument("domain", help="Target domain for DNS enumeration")
    parser.add_argument("--output", type=str, help="Output file to save results (JSON format)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Execute the DNS enumeration function
    try:
        dsnenum(args.domain, output=args.output, verbose=args.verbose)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")
