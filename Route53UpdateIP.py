#!/usr/bin/env python3

import os
import sys
import requests
import boto3
import logging
from dotenv import dotenv_values
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format

# Initialize colorama
init(strip=not sys.stdout.isatty())

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    """Display a cool ASCII art banner."""
    cprint(figlet_format('Route53UpdateIP', font='slant'), 'cyan', attrs=['bold'])

def get_public_ip():
    """Fetch the public IP address."""
    try:
        response = requests.get("https://ipcurl.net/n", verify=False)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch public IP: {e}")
        sys.exit(1)

def read_config():
    """Read configuration from the .conf file."""
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    config_file = f"{script_name}.conf"
    config = dotenv_values(config_file)
    required_keys = ['AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'FQDN']
    
    if not all(key in config for key in required_keys):
        logging.error("Missing required configuration. Please check your .conf file.")
        sys.exit(1)
    
    return config

def update_dns_record(ip_address, config):
    """Update the DNS record if necessary."""
    route53 = boto3.client('route53',
                           region_name=config['AWS_REGION'],
                           aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    try:
        zones = route53.list_hosted_zones_by_name()
        zone_id = next(zone['Id'] for zone in zones['HostedZones'] 
                       if zone['Name'] == f"{config['FQDN']}.")

        records = route53.list_resource_record_sets(HostedZoneId=zone_id)
        current_ip = next(record['ResourceRecords'][0]['Value'] 
                          for record in records['ResourceRecordSets'] 
                          if record['Name'] == f"{config['FQDN']}." 
                          and record['Type'] == 'A')

        if ip_address != current_ip:
            logging.info(f"Updating DNS record for {config['FQDN']} to {ip_address}")
            route53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': config['FQDN'],
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': ip_address}]
                        }
                    }]
                }
            )
            logging.info("DNS record updated successfully")
        else:
            logging.info("IP address unchanged, no update needed")
    except Exception as e:
        logging.error(f"Failed to update DNS record: {e}")
        sys.exit(1)

def main():
    """Main function to orchestrate the DNS update process."""
    display_banner()
    ip_address = get_public_ip()
    config = read_config()
    update_dns_record(ip_address, config)

if __name__ == "__main__":
    main()