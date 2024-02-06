# GoDaddy® Dynamic DNS Updater

This repository contains a Python script for automatically updating DNS records for GoDaddy® domains. The script is ideal for users with dynamic IP addresses who wish to keep their DNS records in sync without manual intervention. There are two versions of the script:

### Version 1 - Scheduled: 
Designed to be run at regular intervals using a scheduler like cron on Linux or Task Scheduler on Windows. (Ideal for machines with limited CPU cores)

### Version 2 - Continuous:
Runs in a continuous loop (through terminal), checking and updating the DNS record if the public IP address changes.

_NOTE: Both are the same code, just different use cases._

# Getting Started
## Prerequisites
* Python 3 installed on your system.
* A GoDaddy® account and [API credentials](https://developer.godaddy.com) (API key and secret).
## Installation
### Clone this repository to your local machine:
```
git clone https://github.com/smalkasian/GoDaddy-Dynamic-DNS.git
```
### Navigate into the cloned directory:
```
cd GoDaddy-Dynamic-DNS
```
### Install required Python libraries:
```
pip install requests
```
# Configuration and Running The Script
* Open the script using a text editor or IDE.
* Locate the VARIABLES section at the top of the script.
* Replace the placeholder values for api_key, api_secret, and domain with your actual GoDaddy® [API credentials](https://developer.godaddy.com) and the domain you wish to update.

### Continuous Version
To run the continuous version, simply execute the script using Python:
```
python godaddy-dynamic-dns_V2-continuous.py
```
_(sometimes you may need to use "python3 godaddy-dynamic-dns_V2-continuous.py")_

The script will continuously check for IP address changes every 5 minutes (default setting) and update the DNS record on GoDaddy® if necessary.

## Version 2 - Scheduled
The scheduled version is intended to be run at regular intervals using a task scheduler. This approach is more resource-efficient and is recommended for most users.

### Scheduling with Cron (Linux)
Open your crontab file for editing:
```
crontab -e
```
Add a line to schedule the script to run at your desired interval. For example, to run every hour:
```
0 * * * * /usr/bin/python /ADD/PATH/TO/godaddy-dynamic-dns_V1-scheduled.py
```
_NOTE: Make sure to add the proper path to the file_

Save and close the crontab.

### Scheduling with Task Scheduler (Windows)
* Open Task Scheduler and create a new task.
* Set the trigger to your desired interval (e.g., every hour).
* For the action, start the program with the script's path as the argument.

### Disclaimer
GoDaddy® is a registered trademark of GoDaddy Operating Company, LLC. This project is not affiliated with, endorsed by, or sponsored by GoDaddy Operating Company, LLC.
