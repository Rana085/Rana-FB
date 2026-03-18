import os, sys, time, random, string, re, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Theme Colors (Akatsuki Style)
R, G, Y, C, W, S = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;36m', '\033[1;37m', '\033[0m'

# --- CONFIGURATION ---
VERSION = "16.1"
# Update URL: Replace this with your raw GitHub script URL later
UPDATE_URL = "https://raw.githubusercontent.com/YourUsername/FB-MASTER/main/version.txt" 
proxies = []

def check_update():
    """Checks for updates and notifies the user"""
    print(f'{C}[*] Checking for system updates...{S}')
    try:
        # For now, it's a simulation. You can link your GitHub here.
        latest_version = "16.1" 
        if latest_version > VERSION:
            print(f'{G}[!] New Update Available! Version: {latest_version}{S}')
            print(f'{Y}[*] Please update your script from GitHub.{S}')
            time.sleep(2)
        else:
            print(f'{G}[√] Your system is up to date.{S}')
    except:
        print(f'{R}[!] Could not reach the update server.{S}')

def get_ua():
    versions = ["12", "13", "14"]
    models = ["SM-S918B", "Pixel 8", "OnePlus 11", "Xiaomi 13 Ultra"]
    return f"Mozilla/5.0 (Linux; Android {random.choice(versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"

def scrape_proxies():
    global proxies
    print(f'{Y}[*] Fetching fresh proxy list...{S}')
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000').text
        proxies = res.strip().split('\r\n')
        print(f'{G}[√] Loaded {len(proxies)} proxies.{S}')
    except:
        print(f'{R}[X] Proxy fetch failed. Continuing without proxies.{S}')

def get_email():
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=10)
        if res.status_code == 200:
            return res.json()[0]
    except:
        return None

def create_account(t_id):
    email = get_email()
    if not email:
        print(f'{R}[T-{t_id}] Email Server Busy. Retrying...{S}')
        return
    
    password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    print(f'{C}[Thread-{t_id}] {W}Target: {G}{email}{S}')

    session = requests.Session()
    session.headers.update({'User-Agent': get_ua()})
    
    if proxies:
        p = random.choice(proxies)
        session.proxies = {'http': f'http://{p}', 'https': f'http://{p}'}

    try:
        resp = session.get("https://mbasic.facebook.com/reg/", timeout=15).text
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Gathering hidden tokens dynamically
        data = {i.get('name'): i.get('value') for i in soup.find_all('input', type='hidden') if i.get('name')}
        data.update({
            'firstname': 'Itachi', 'lastname': 'Uchiha',
            'reg_email__': email, 'reg_passwd__': password,
            'birthday_day': str(random.randint(1,28)),
            'birthday_month': str(random.randint(1,12)),
            'birthday_year': str(random.randint(1992, 2004)), 'sex': '2'
        })

        submit = session.post("https://mbasic.facebook.com/reg/submit/", data=data, timeout=15)

        if "checkpoint" in submit.url:
            print(f'{R}[T-{t_id}] Security Checkpoint (IP Blocked).{S}')
        elif "captcha" in submit.text.lower():
            print(f'{Y}[T-{t_id}] Captcha encountered. Moving to next...{S}')
        else:
            print(f'{G}[T-{t_id}] Account Form Submitted Successfully!{S}')
            with open('Success_IDs.txt', 'a') as f:
                f.write(f'Email: {email} | Pass: {password}\n')
            
    except:
        print(f'{R}[T-{t_id}] Connection Timeout.{S}')

def main_menu():
    os.system('clear')
    print(f"""{R}
    FB-AUTO MASTER [VERSION {VERSION}]
    {W}-------------------------------------------
    {G}[1] Start Auto Creation
    {Y}[2] Check for Updates
    {R}[0] Exit
    {W}-------------------------------------------{S}""")
    
    choice = input(f"{Y}[?] Option: {S}")
    if choice == '1':
        scrape_proxies()
        print(f'\n{G}[+] Engine Started. Press Ctrl+C to stop.{S}\n')
        with ThreadPoolExecutor(max_workers=2) as executor:
            for i in range(1, 1000):
                executor.submit(create_account, i)
                time.sleep(10)
    elif choice == '2':
        check_update()
        input(f"\n{C}[!] Press Enter to return...{S}")
        main_menu()
    else:
        sys.exit()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(f'\n{R}[!] Stopping Tool...{S}')
