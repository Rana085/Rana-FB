import os, sys, time, random, string, re, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Akatsuki Theme Color Settings
R = '\033[1;31m' # Red
G = '\033[1;32m' # Green
Y = '\033[1;33m' # Yellow
C = '\033[1;36m' # Cyan
W = '\033[1;37m' # White
S = '\033[0m'    # Reset

proxies = []

# Dynamic User Agent Generator
def get_ua():
    return f"Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"

# Free Proxy Scraper
def scrape_proxies():
    global proxies
    print(f'{Y}[*] Scraping proxies... Please wait.{S}')
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&anonymity=elite')
        proxies = res.text.strip().split('\r\n')
        if proxies and proxies[0]:
            print(f'{G}[√] Total active proxies found: {len(proxies)}{S}')
        else:
            proxies = []
            print(f'{R}[X] No proxies found!{S}')
    except Exception as e:
        print(f'{R}[X] Proxy server error: {e}{S}')

# Temp Mail Generator
def get_email():
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox", timeout=10)
        return res.json()[0]
    except Exception as e:
        print(f'{R}[!] Email server down: {e}{S}')
        return None

# Main Account Creation Engine
def create_account(t_id):
    email = get_email()
    if not email: return
    
    password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    print(f'{C}[Thread-{t_id}] {W}Creating account: {G}{email}{S}')

    session = requests.Session()
    session.headers.update({'User-Agent': get_ua()})
    
    if proxies:
        p = random.choice(proxies)
        session.proxies = {'http': f'http://{p}', 'https': f'http://{p}'}

    try:
        # Load mbasic registration page
        resp = session.get("https://mbasic.facebook.com/reg/", timeout=15).text
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Extract hidden tokens
        data = {i.get('name'): i.get('value') for i in soup.find_all('input', type='hidden') if i.get('name')}
        data.update({
            'firstname': 'Itachi', 'lastname': 'Uchiha',
            'reg_email__': email, 'reg_passwd__': password,
            'birthday_day': str(random.randint(1,28)),
            'birthday_month': str(random.randint(1,12)),
            'birthday_year': str(random.randint(1995, 2005)), 'sex': '2'
        })

        # Submit registration
        submit = session.post("https://mbasic.facebook.com/reg/submit/", data=data, timeout=15)

        if "checkpoint" in submit.url:
            print(f'{R}[T-{t_id}] Checkpoint! (IP Blocked - Toggle Airplane Mode){S}')
        elif "captcha" in submit.text.lower() or "security" in submit.text.lower():
            print(f'{Y}[T-{t_id}] Captcha Detected! Skipping thread...{S}')
        else:
            print(f'{G}[T-{t_id}] Submit successful! Waiting for OTP...{S}')
            # OTP Logic goes here
            
    except Exception as e:
        print(f'{R}[T-{t_id}] Connection error (Proxy or Network issue){S}')

# Automation Starter
def start_auto():
    scrape_proxies()
    print(f'\n{G}[+] Bot started. Press Ctrl+C to stop.{S}\n')
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(1, 100):
            executor.submit(create_account, i)
            time.sleep(5) # 5 seconds delay between attempts

# Main Menu
def main_menu():
    os.system('clear')
    print(f"""{R}
    ███████╗██████╗      █████╗ ██╗   ██╗████████╗ ██████╗ 
    ██╔════╝██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
    █████╗  ██████╔╝    ███████║██║   ██║   ██║   ██║   ██║
    ██╔══╝  ██╔══██╗    ██╔══██║██║   ██║   ██║   ██║   ██║
    ██║     ██████╔╝    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝     ╚═════╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
    {W}[ VERSION: 16.0 - ZERO BUDGET EDITION ]{S}
    """)
    print(f"{C}[ 1 ] {W}Start Auto Create")
    print(f"{C}[ 2 ] {W}Check Proxies")
    print(f"{C}[ 0 ] {W}Exit{S}\n")
    
    choice = input(f"{Y}[?] Enter your choice (0/1/2): {S}")
    
    if choice == '1':
        start_auto()
    elif choice == '2':
        scrape_proxies()
        input(f"\n{C}[!] Press Enter to return to the main menu...{S}")
        main_menu()
    elif choice == '0':
        sys.exit(f'\n{R}[!] Tool stopped successfully.{S}')
    else:
        main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(f'\n{R}[!] Tool manually stopped.{S}')
