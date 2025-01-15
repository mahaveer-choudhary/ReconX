from colorama import Fore, Style, init
import sys
import os
import time
import asyncio
from modules import dnsenum
from modules import whois_enum
from modules import ssh_bruteforcer
from modules import ftp_bruteforcer
from modules import service_scanner
from modules import bypasser
from modules import subdomain
from modules import hash_cracker
from modules import web_enumerator


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    init(autoreset=True)
    # print(f"{Fore.GREEN}Mahaveer's framwork{Fore.RESET}")
    def print_logo():
        logo = f"""
    {Fore.RED}{Style.BRIGHT}
                    >>================================<<
                    ||                                ||
                    ||   ,-.                  .   ,   ||
                    ||   |  )                  \\ /    ||
                    ||   |-<  ,-. ,-. ,-. ;-.   X     ||
                    ||   |  \\ |-' |   | | | |  / \\    ||
                    ||   '  ' `-' `-' `-' ' ' '   `   ||
                    ||                                ||
                    >>================================<<
"""
        print(logo)

    print_logo()

    print()
    while True : 
        print(f"{Fore.BLUE}Which Tool you want to use? ")
        tools_menu = ("""
            1. DNS Enumeration
            2. Whois Recon
            3. SSH BruteForce
            4. FTP BruteForce
            5. Service Scanner
            6. 403 bypasser
            7. Subdomain Enumeration
            8. Hash Cracker
            9. Web Enumerator
            0. Exit
        """)
        print(f"{Fore.GREEN}{tools_menu}{Fore.RESET}")

        while True : 
            try : 
                choose = input(f"{Fore.BLUE}Enter the number of tool you want to use : {Fore.RESET}").strip()

                if not choose.isdigit():
                    raise ValueError(f"{Fore.RED}Input must be an number..{Fore.RESET}")

                choose = int(choose)

                if choose < 0 or choose > 9 : 
                    raise ValueError(f"{Fore.RED}you can't choose out of tool's number. (must be between 1-9){Fore.RESET}")

                break
            
            except ValueError as e : 
                print(f"{Fore.RED}Error : {e} Please try agian..")

        
        if choose == 0 :
            print(f"{Fore.CYAN}Please wait a sec. You are exiting the framework.")
            time.sleep(1)
            # clear_screen()
            # sys.exit(1)
            break

        elif choose == 1 : 
            # print("Hello mahaveer...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed DNS Enumeration Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            ## call the dns-enumeration modules 
            print(f"{Fore.GREEN}starting DNS Enumeration tool {Fore.RESET}")
            domain = input(f"Enter the domain name to enumerate : ").strip()
            output_file = input(f"Enter the output file name (leave blank to skip saving) : ").strip()

            try : 
                dnsenum.dsnenum(domain, output_file)
                print(f"{Fore.GREEN}DNS Enumeration completed successfully.. {Fore.RESET}\n\n")

                main_menu = input(f"{Fore.CYAN}Do you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e : 
                print(f"{Fore.RED}Error running DNS enumeration : {e} {Fore.RESET}\n\n")
            
        
        elif choose == 2 : 
            # print("hello mahaveer...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed WHOIS Recon Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            ## call the whois enumeration module 
            print(f"{Fore.GREEN}starting WHOIS Enumeration tool {Fore.RESET}")
            domain = input(f"Enter the domain name to enumerate : ").strip()
            output_file = input(f"Enter the output file name (leave blank to skip saving) : ").strip()

            try : 
                whois_enum.whois_recon(domain, output_file)
                print(f"{Fore.GREEN}WHOIS Enumeration completed successfully.. {Fore.RESET}\n\n")

                main_menu = input(f"{Fore.CYAN}Do you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e : 
                print(f"{Fore.RED}Error running WHOIS Enumeration : {e} {Fore.RESET}\n\n")

        
        elif choose == 3 : 
            # print("Hello mahaveer...")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed SSH Brutefocer Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            ## call the ssh bruteforcer module 
            print(f"{Fore.GREEN}starting the SSH Bruteforcer tool {Fore.RESET}")
            hostname = input(f"Enter the hostname (ex - 10.10.10.10): ").strip()
            username = input(f"Enter the username : ").strip()
            port = input(f"Enter the port number (skip for default port 22) : ").strip()
            wordlist = input(f"Enter the path of the wordlist : ").strip()

            port = int(port) if port.isdigit() else 22

            try : 
                # ssh_bruteforcer.main(hostname, port, username, wordlist)
                asyncio.run(ssh_bruteforcer.main(hostname, port, username, wordlist))
                print(f"{Fore.GREEN}SSH Bruteforce completed successfully..{Fore.RESET}\n\n")

                main_menu =  input(f"{Fore.CYAN}Do you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e : 
                print(f"{Fore.RED}Error running SSH Bruteforcer tool. {e} {Fore.RESET}\n\n")

        elif choose == 4 : 
            # print("Hello mahaveer...")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed FTP Bruteforcer Tool..")
            print(f"{Fore.CYAN}wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            ## calling the ftp bruteforcer module
            print(f"{Fore.GREEN}starting the SSH BruteForcer tool {Fore.RESET}")
            hostname = input(f"Enter the hostname (ex - 10.10.10.10): ").strip()
            username = input(f"Enter the username : ").strip()
            port = input(f"Enter the port number (skip for default port 21) : ").strip()
            wordlist = input(f"Enter the path of the wordlist : ").strip()

            port = int(port) if port.isdigit() else 21

            try : 
                ftp_bruteforcer.main(hostname, int(port), username, wordlist)
                print(f"{Fore.GREEN}FTP Bruteforce completed successfully..{Fore.RESET}\n\n")

                main_menu = input(f"{Fore.CYAN}Do you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n') :
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e : 
                print(f"{Fore.RED}Error running FTP Bruteforcer tool. {e} {Fore.RESET}\n\n")

        elif choose == 5 : 
            # print("Hello mahaveer... ")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed Service Scanner Tool..")
            print(f"{Fore.CYAN}wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            target = input("Enter the target hostname or IP (e.g., 127.0.0.1): ").strip()
            start_port = int(input("Enter the start port (default 1): ").strip() or 1)
            end_port = int(input("Enter the end port (default 1024): ").strip() or 1024)
            threads = int(input("Enter the number of threads (default 10): ").strip() or 10)

            try:
                service_scanner.main(target, start_port, end_port, threads)
                print(f"{Fore.GREEN}Service scanning completed successfully.{Fore.RESET}")
                
                main_menu = input(f"{Fore.CYAN}Do you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n') :
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e:
                print(f"{Fore.RED}Error running Service Scanner tool: {e}{Fore.RESET}")

        elif choose == 6 : 
            # print("Hello mahaveer...")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed 403 Bypasswer Tool..")
            print(f"{Fore.CYAN}wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            url = input(f"{Fore.BLUE}Enter the url to bypass it : ").strip()

            print(f"{Fore.CYAN}Choose a bypass mode ->")
            a = ("""
                1. Header Bypass
                2. Protocol Bypass
                3. Port Bypass 
                4. HTTP Method Bypass 
                5. URL Encode Bypass
                6. Full Exploit (All Bypasses)
            """)
            print(f"{Fore.GREEN}{a}")
            bypass_mode = input(f"{Fore.CYAN}Enter the bypass mode method (1-6) : ").strip()
            try : 
                if bypass_mode == '1' : 
                    bypasser.header_bypass(url)
                elif (bypass_mode == '2') : 
                    bypasser.protocol_bypass(url)
                elif (bypass_mode == '3'): 
                    bypasser.port_bypass(url)
                elif (bypass_mode == '4'): 
                    bypasser.http_method_bypass(url)
                elif (bypass_mode == '5'): 
                    bypasser.url_encode_bypass(url)
                elif (bypass_mode == '6'): 
                    bypasser.bypass_403(url)
                else : 
                    print(f"{Fore.RED}Invalid choice. Returning to main menu.{Fore.RESET}")
                    continue

                main_menu = input(f"{Fore.CYAN}\nDo you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n') :
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            except Exception as e : 
                print(f"{Fore.RED}Error running 403 bypasser tool : {e} {Fore.RESET}")

        elif choose == 7 : 
            # print("Hello mahaveer...")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed Subdomain Enumeration Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            try : 
                subdomain.main()
                print(f"{Fore.GREEN}Subdomain Enumeration completed successfully.\n{Fore.RESET}")

                main_menu = input(f"{Fore.CYAN}\nDo you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)

            except Exception as e : 
                print(f"{Fore.RED}Error running Subdomain Enumeration tool : {e}\n {Fore.RESET}")

        elif choose == 8 : 
            # print("Hello mahaveer...")
            # print("Tool is under working...")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed Hash Cracker Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            hash_value = input("Enter the hash value to crack : ").strip()
            ## optional inputs 
            hash_type = input("Enter the hash type (md5, sha1, sha256 - leave blank to auto-detect) : ").strip().lower()
            wordlist_path = input("Enter the path of your wordlist file(leave blank for default) : ").strip()
            threads = input("Enter the number of threads (default is 4) : ").strip()

            hash_type = hash_type if hash_type else None
            # wordlist_path = wordlist_path if wordlist_path else "word.txt"
            wordlist_path = wordlist_path if wordlist_path else None
            threads = int(threads) if threads.isdigit() else 4

            try : 
                # if hash_type : 
                #     hash_cracker.main(hash_value, wordlist_path, threads, hash_type)
                # else : 
                #     hash_cracker.main(hash_value, wordlist_path, threads)
                hash_cracker.main(hash_value=hash_value, wordlist=wordlist_path, thread_count=threads)
                print(f"{Fore.GREEN}Hash Cracker Completed successfully.\n{Fore.RESET}")

                main_menu = input(f"{Fore.CYAN}\nDo you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            
            except Exception as e : 
                print(f"{Fore.RED}Error running Hash Cracker tool : {e} {Fore.RESET}")

        elif choose == 9 : 
            # print("Hello mahaveer...")
            # print("Tool is under working..")
            print(f"{Fore.LIGHTMAGENTA_EX}You choosed Web Enumerator Tool..")
            print(f"{Fore.CYAN}Wait a second. Starting the tool...")
            time.sleep(1)
            clear_screen()

            try : 
                url = input(f"Enter the url for scan : ").strip()
                web_enumerator.run_web_server_enumeration(url)
                print(f"{Fore.GREEN}Web Enumeration completed successfully.\n{Fore.RESET}")

                main_menu = input(f"{Fore.CYAN}\nDo you want to go back to main menu (Y/N) : ").strip().lower()
                if (main_menu == 'y'): 
                    continue
                elif (main_menu == 'n'): 
                    print(f"{Fore.RED}Exiting the framework...")
                    sys.exit(1)
            
            except Exception as e : 
                print(f"{Fore.RED}Error running Web Server Enumeration tool : {e}\n {Fore.RESET}")

        else : 
            print("Sorry mahaveer.. you choose wrong number.. try again.")


if __name__ == "__main__":
    main()