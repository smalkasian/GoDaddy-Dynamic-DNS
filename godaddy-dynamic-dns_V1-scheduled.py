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
api_key = 'REPLACE_WITH_YOUR_KEY'
api_secret = "REPLACE_WITH_YOUR_SECRET"
domain = 'example.com'

record_type = 'A'
record_name = '@'
ip_file = 'last_ip.txt'
headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "Content-Type": "application/json"
}
#--------------------------------------FUNCTIONS------------------------------------------
def get_public_ip():
    # List of services to get the public IP address. Add or remove services as needed.
    services = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip"
    ]
    for service in services:
        try:
            response = requests.get(service, timeout=5)  # Added a timeout for the request
            if response.status_code == 200:
                return response.text.strip()
        except requests.RequestException as e:
            print(f"Error fetching public IP address from {service}: {e}")
    return None

def get_current_dns_ip():
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()
        if records:
            return records[0]['data']
    return None

def update_dns(new_ip_address, attempts=0):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}"
    data = [{"data": new_ip_address, "ttl": 600}]
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 429 and attempts < 5:  # Too Many Requests
        wait_time = 2 ** attempts  # Exponential backoff
        print(f"Rate limit reached, retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        update_dns(new_ip_address, attempts + 1)  # Retry with increased backoff
    elif response.status_code == 200:
        print("DNS record updated successfully.")
    else:
        print(f"Failed to update DNS record. Status code: {response.status_code}, Response: {response.text}")

def main():
    new_ip_address = get_public_ip()
    if not new_ip_address:
        print("Failed to retrieve public IP address.")
        return

    current_dns_ip = get_current_dns_ip()
    if current_dns_ip is None:
        print("Failed to fetch current DNS IP. Exiting...")
        return

    if new_ip_address != current_dns_ip:
        print(f"IP address has changed to {new_ip_address}. Updating DNS...")
        update_dns(new_ip_address)
    else:
        print("IP address has not changed. No update needed.")

#------------------------------------MAIN PROGRAM-----------------------------------------
        
if __name__ == "__main__":
    main()
