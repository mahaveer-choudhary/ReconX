# ReconX

ReconX is a Python-based multi-tool framework designed for penetration testing, enumeration, and brute-forcing. It allows security professionals and researchers to perform various security tasks like DNS enumeration, SSH brute-force, FTP brute-force, web server enumeration, and more with ease. The framework includes several modules that help in performing different tasks, offering flexibility and effectiveness for different use cases.

## Features

1. **DNS Enumeration Tool** - Enumerates DNS records for a given domain.
2. **WHOIS Recon Tool** - Retrieves WHOIS information for a domain.
3. **SSH Bruteforce Tool** - Performs SSH brute-forcing on a target host.
4. **FTP Bruteforce Tool** - Performs FTP brute-forcing on a target host.
5. **Service Scanner Tool** - Scans ports and identifies services running on them.
6. **403 Bypasser Tool** - Bypasses HTTP 403 restrictions using multiple techniques.
7. **Subdomain Enumeration Tool** - Performs subdomain enumeration for a given domain.
8. **Hash Cracker Tool** - Cracks various types of hashes using a wordlist.
9. **Web Enumerator Tool** - Performs web server enumeration to gather information about web servers.

## Requirements

To run this framework, you need Python 3.6+ installed on your system along with the following dependencies:

- `colorama`
- `asyncio`

You can install the necessary dependencies by running:

```bash
pip install colorama
pip install asyncio
```

## How to use

### Clone the Repository:

```bash
git clone https://github.com/mahaveer-choudhary/ReconX.git
cd ReconX
```
### Install requirements

```bash
pip3 install -r requirements.txt
```
### Run the Script:

You can run the script directly using Python. It will provide you options to select the tool you want to use. 

### for linux
```bash
python3 main.py
```

### for windows 
```bash
python main.py
```

### Disclaimer
This framework is for educational and testing purposes only. Always have proper authorization before performing any form of penetration testing or scanning on systems you do not own or have explicit permission to test.