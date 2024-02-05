#------------------------------------------------------------------------------------
# Developed by MalkasianGroup, LLC - Open Source DNS updater for GoDaddy® Domains.
# Free for personal use only – for enterprise or business use, please email malkasian(a)dsm.studio
#------------------------------------------------------------------------------------
# Legal stuff:
# GoDaddy® is a registered trademark of GoDaddy Operating Company, LLC. All rights reserved.
#------------------------------------------------------------------------------------


import requests
import time

#--------------------------------------VARIABLES------------------------------------------
# These are the ONLY three variables you need to replace
API_KEY = '1234'  # Replace with your actual API key
API_SECRET = "1234"  # Replace with your actual API secret
DOMAIN = 'malkasian.org'  # Replace with your actual domain
RECORD_TYPE = 'A'
RECORD_NAME = '@'
CHECK_INTERVAL = 300

headers = {
    "Authorization": f"sso-key {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

#--------------------------------------FUNCTIONS------------------------------------------
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text if response.status_code == 200 else None
    except Exception as e:
        print(f"Error fetching public IP address: {e}")
        return None

def get_current_dns_ip():
    url = f"https://api.godaddy.com/v1/domains/{DOMAIN}/records/{RECORD_TYPE}/{RECORD_NAME}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()
        if records:
            return records[0]['data']
    return None

def update_dns(new_ip_address, attempts=0):
    if attempts >= 5:
        print("Maximum retry attempts reached. Exiting...")
        return
    url = f"https://api.godaddy.com/v1/domains/{DOMAIN}/records/{RECORD_TYPE}/{RECORD_NAME}"
    data = [{"data": new_ip_address, "ttl": 600}]
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 429:  # Too Many Requests
        wait_time = 2 ** attempts  # Exponential backoff
        print(f"Rate limit reached, retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        update_dns(new_ip_address, attempts + 1)
    elif response.status_code == 200:
        print("DNS record updated successfully.")
    else:
        print(f"Failed to update DNS record. Status code: {response.status_code}, Response: {response.text}")

def main_loop():
    while True:
        new_ip_address = get_public_ip()
        if not new_ip_address:
            print("Failed to retrieve public IP address.")
            time.sleep(CHECK_INTERVAL)
            continue
        current_dns_ip = get_current_dns_ip()
        if new_ip_address != current_dns_ip:
            print(f"IP address has changed to {new_ip_address}. Updating DNS...")
            update_dns(new_ip_address)
        else:
            print("IP address has not changed. No update needed.")
        time.sleep(CHECK_INTERVAL)

#------------------------------------MAIN PROGRAM-----------------------------------------
        
if __name__ == "__main__":
    main_loop()
