#!/usr/bin/env python3

import argparse
import re
import os
import requests
import hashlib
import concurrent.futures
import urllib3

try:
    import websocket
    websocket_available = True
except ImportError:
    websocket_available = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Colors for console output
end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'
bad = '\033[91m[-]\033[0m'

# Hash cracking methods
def alpha(hashvalue, hashtype):
    """ Uses cmd5.org for hash decryption """
    cookies = {'ASP.NET_SessionId': 'be2jpjuviqbaa2mmq1w4h5ci'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {
        '__EVENTTARGET': 'Button1',
        '__VIEWSTATE': '6fEUcEEj0b0eN1Obqeu4TSsOBdS0APqz...',
        'ctl00$ContentPlaceHolder1$TextBoxInput': hashvalue,
        'ctl00$ContentPlaceHolder1$InputHashType': hashtype,
        'ctl00$ContentPlaceHolder1$Button1': 'decrypt',
    }
    try:
        response = requests.post('https://www.cmd5.org/', cookies=cookies, headers=headers, data=data)
        match = re.search(r'<span id="LabelAnswer"[^>]+?>(.+)</span>', response.text)
        return match.group(1) if match else False
    except requests.RequestException:
        return False

def beta(hashvalue, hashtype):
    """ Uses md5hashing.net WebSocket for hash decryption """
    if not websocket_available:
        print(f'{red} WebSocket module not available, skipping beta method.{end}')
        return False

    url = "wss://md5hashing.net/sockjs/697/etstxji0/websocket"
    try:
        ws = websocket.create_connection(url)
        connect_message = r'[{"msg":"connect","version":"1","support":["1","pre2","pre1"]}]'
        ws.send(connect_message)
        method_message = r'[{"msg":"method","method":"hash.get","params":["{}","{}"],"id":"1"}]'.format(hashtype, hashvalue)
        ws.send(method_message)
        response = ws.recv()
        match = re.search(r'"value":"([^"]+)"', response)
        return match.group(1) if match else False
    except Exception:
        return False

def gamma(hashvalue, hashtype):
    """ Uses nitrxgen.net for hash decryption """
    try:
        response = requests.get(f'https://www.nitrxgen.net/md5db/{hashvalue}', verify=False).text
        return response if response else False
    except requests.RequestException:
        return False

def theta(hashvalue, hashtype):
    """ Uses md5decrypt.net API for hash decryption """
    try:
        api_url = f'https://md5decrypt.net/Api/api.php?hash={hashvalue}&hash_type={hashtype}&email=example@example.com&code=examplecode'
        response = requests.get(api_url).text
        return response if response else False
    except requests.RequestException:
        return False

def hash_word(word, hashtype):
    """ Hashes a word using the specified hash type (MD5, SHA1, etc.) """
    if hashtype == 'md5':
        return hashlib.md5(word.encode('utf-8')).hexdigest()
    elif hashtype == 'sha1':
        return hashlib.sha1(word.encode('utf-8')).hexdigest()
    elif hashtype == 'sha256':
        return hashlib.sha256(word.encode('utf-8')).hexdigest()
    elif hashtype == 'sha384':
        return hashlib.sha384(word.encode('utf-8')).hexdigest()
    elif hashtype == 'sha512':
        return hashlib.sha512(word.encode('utf-8')).hexdigest()
    return None

def wordlist_crack(hashvalue, wordlist_path, hashtype):
    """ Attempts to crack the hash by checking each word in the wordlist """
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            for word in f:
                word = word.strip()
                hashed_word = hash_word(word, hashtype)
                if hashed_word == hashvalue:
                    return word
    except Exception as e:
        print(f"{bad} Error reading wordlist: {e}")
    return False

def crack(hashvalue, wordlist_path=None):
    """ Determines hash type and attempts to crack it using available methods, including wordlist cracking """
    hash_methods = {
        32: ('md5', [alpha, beta, gamma, theta]),
        40: ('sha1', [alpha, beta, theta]),
        64: ('sha256', [alpha, beta, theta]),
        96: ('sha384', [alpha, beta, theta]),
        128: ('sha512', [alpha, beta, theta])
    }
    hash_length = len(hashvalue)
    if hash_length in hash_methods:
        hashtype, methods = hash_methods[hash_length]
        print(f'{info} Hash type detected: {hashtype}')

        # First, try methods
        for method in methods:
            result = method(hashvalue, hashtype)
            if result:
                return result

        # Then, try wordlist cracking if a wordlist is provided
        if wordlist_path:
            print(f'{info} Attempting wordlist cracking using wordlist: {wordlist_path}')
            result = wordlist_crack(hashvalue, wordlist_path, hashtype)
            if result:
                return result

    return False

def threaded(hashvalue, results):
    """ Executes the crack function in a thread """
    result = crack(hashvalue)
    if result:
        print(f'{green}{hashvalue} : {result}{end}')
        results[hashvalue] = result

def grepper(directory):
    """ Searches for hash-like patterns in a directory """
    found_hashes = set()
    for root, _, files in os.walk(directory):
        for file in files:
            try:
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()
                    matches = re.findall(r'[a-f0-9]{32,128}', content)
                    found_hashes.update(matches)
            except Exception:
                pass
    print(f'{info} Found {len(found_hashes)} hashes.')
    return found_hashes

def miner(file, thread_count, results):
    """ Reads hashes from a file and processes them """
    with open(file, 'r') as f:
        hashes = {line.strip() for line in f if re.match(r'[a-f0-9]{32,128}', line.strip())}
    print(f'{info} Found {len(hashes)} hashes in file.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(lambda h: threaded(h, results), hashes)

def single(hashvalue, wordlist=None):
    """ Cracks a single hash """
    result = crack(hashvalue, wordlist)
    if result:
        print(f'{good} {result}')
    else:
        print(f'{bad} Hash not found.')

def main(hash_value=None, file=None, directory=None, wordlist=None, thread_count=4):
    """ Main function for hash cracking, now supports wordlist-based cracking """
    results = {}
    if directory:
        hashes = grepper(directory)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            executor.map(lambda h: threaded(h, results), hashes)
    elif file:
        miner(file, thread_count, results)
    elif hash_value:
        # If wordlist is provided, pass it to the crack function
        if wordlist:
            result = crack(hash_value, wordlist)
            if result:
                print(f'{green}{hash_value} : {result}{end}')
            else:
                print(f'{bad} Hash not found in wordlist.{end}')
        else:
            single(hash_value)

    # Save results
    if results:
        output_file = 'cracked_hashes.txt'
        with open(output_file, 'w') as f:
            for hashvalue, result in results.items():
                f.write(f'{hashvalue} : {result}\n')
        print(f'{info} Results saved in {output_file}')

    print(f'{info} Hash cracking completed.')

if __name__ == "__main__":
    # Argument parser for standalone execution
    parser = argparse.ArgumentParser(description="Hash Cracking Framework")
    parser.add_argument("--hash", help="Single hash to crack", dest="hash")
    parser.add_argument("--file", help="File containing hashes", dest="file")
    parser.add_argument("--dir", help="Directory containing hashes", dest="dir")
    parser.add_argument("--wordlist", help="Wordlist file for cracking", dest="wordlist")
    parser.add_argument("--threads", help="Number of threads (default: 4)", dest="threads", type=int, default=4)

    args = parser.parse_args()
    main(hash_value=args.hash, file=args.file, directory=args.dir, wordlist=args.wordlist, thread_count=args.threads)
