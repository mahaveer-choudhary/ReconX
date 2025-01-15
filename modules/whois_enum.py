import whois
import json
from colorama import Fore

def whois_recon(domain, output=None, verbose=False):
    """
    Perform WHOIS Reconnaissance on the given domain.

    Args:
        domain (str): The target domain name.
        output (str, optional): File name to save the output. Defaults to None.
        verbose (bool, optional): Enable verbose output. Defaults to False.
    """
    try:
        print(f"{Fore.CYAN}Fetching WHOIS information for {Fore.YELLOW}{domain}{Fore.RESET}...")
        w = whois.whois(domain)  # Perform the WHOIS lookup
        
        # Convert the WHOIS data to a dictionary
        whois_data = {
            "Domain Name": w.domain_name,
            "Registrar": w.registrar,
            "Whois Server": w.whois_server,
            "Updated Date": str(w.updated_date),
            "Creation Date": str(w.creation_date),
            "Expiration Date": str(w.expiration_date),
            "Name Servers": w.name_servers,
            "Status": w.status,
            "Emails": w.emails,
            "Country": w.country,
            "Organization": w.org,
        }
        
        # Display the WHOIS data
        print(f"{Fore.GREEN}WHOIS Data for {domain}:{Fore.RESET}\n")
        for key, value in whois_data.items():
            if verbose or value:  # Show only available data unless verbose is True
                print(f"{Fore.YELLOW}{key}:{Fore.BLUE} {value}{Fore.RESET}")
        
        # Save the data to a JSON file if output is specified
        if output:
            with open(output, "w") as f:
                json.dump(whois_data, f, indent=4)
            print(f"\n{Fore.GREEN}WHOIS data saved to {Fore.YELLOW}{output}{Fore.RESET}")
        
    except Exception as e:
        print(f"{Fore.RED}Error performing WHOIS lookup: {e}{Fore.RESET}")
