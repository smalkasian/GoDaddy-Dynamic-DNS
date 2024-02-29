#------------------------------------------------------------------------------------
# Developed by MalkasianGroup, LLC - Open Source DNS updater for GoDaddy® Domains.
# Free for personal use only – for enterprise or business use, please email malkasian(a)dsm.studio
#------------------------------------------------------------------------------------
# Legal stuff:
# GoDaddy® is a registered trademark of GoDaddy Operating Company, LLC. All rights reserved.
#------------------------------------------------------------------------------------
from requests.exceptions import RequestException
import requests
import time
from datetime import datetime

#--------------------------------------VARIABLES------------------------------------------
API_KEY = '1234'  # Replace with your actual API key
API_SECRET = "1234"  # Replace with your actual API secret
DOMAINS = ['example1.com', 'example2.com']  # Replace with your actual domains. (Note: If you only have one domain, leave only ONE in the list.)
RECORD_TYPE = 'A'
RECORD_NAME = '@'
CHECK_INTERVAL = 300

headers = {
    "Authorization": f"sso-key {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

#--------------------------------------FUNCTIONS------------------------------------------

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_public_ip():
    services = ["https://api.ipify.org", "https://icanhazip.com", "https://ifconfig.me/ip"]
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except requests.RequestException as e:
            print(f"Error fetching public IP address from {service}: {e}")
    return None

def get_current_dns_ip(domain):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{RECORD_TYPE}/{RECORD_NAME}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()
        if records:
            return records[0]['data']
    return None

def update_dns(domain, new_ip_address, attempts=0):
    if attempts >= 5:
        print("Maximum retry attempts reached. Exiting...")
        return
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{RECORD_TYPE}/{RECORD_NAME}"
    data = [{"data": new_ip_address, "ttl": 600}]
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 429:
        wait_time = 2 ** attempts
        print(f"Rate limit reached, retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        update_dns(domain, new_ip_address, attempts + 1)
    elif response.status_code == 200:
        print(f"DNS record for {domain} updated successfully.")
    else:
        print(f"Failed to update DNS record for {domain}. Status code: {response.status_code}, Response: {response.text}")

def check_and_update_domain(domain):
    new_ip_address = get_public_ip()
    if not new_ip_address:
        current_time = get_current_time()
        print(f"Failed to retrieve public IP address. {current_time}")
        return
    current_dns_ip = get_current_dns_ip(domain)
    if new_ip_address != current_dns_ip:
        current_time = get_current_time()
        print(f"IP changed to {new_ip_address} for {domain}. Updating DNS... {current_time}")
        update_dns(domain, new_ip_address)
    else:
        current_time = get_current_time()
        print(f"IP not changed for {domain}. No update needed. {current_time}")

def main_loop():
    while True:
        try:
            for domain in DOMAINS:
                check_and_update_domain(domain)
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError occurred: {e}. Retrying in {CHECK_INTERVAL} seconds...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            time.sleep(CHECK_INTERVAL)

#------------------------------------MAIN PROGRAM-----------------------------------------

if __name__ == "__main__":
    main_loop()
