#!/usr/bin/env python3
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
'''
STEVE SPLASH CODES (@whiteshepherdsec | @whiteshepherdse)
THIS SCRIPT IS CREATED FOR GOOD USE ONLY!
REMEMBER TO BE ETHICAL AS PERFORMING ATTACKS IN AN UNAUTHORIZE ENVIRONMENT CAN PUT IN JAIL! USE AT YOUR OWN RISK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
exit(;)
'''
def read_targets(target_file):
    with open(target_file, 'r', encoding='utf-8') as file:
        return [target.strip() for target in file.readlines()]

def run_dnsrecon(target, output_folder):
    output_file = os.path.join(output_folder, 'dnsrecon', f'{target}_dnsrecon.json')
    command = f'dnsrecon -d {target} -a -j {output_file}'
    print(f'[INFO] Running dnsrecon on {target}')
    os.system(command)

def run_dnsenum(target, output_folder):
    output_file = os.path.join(output_folder, 'dnsenum', f'{target}_dnsenum.txt')
    command = f'dnsenum --dnsserver 8.8.8.8 --output {output_file} {target}'
    print(f'[INFO] Running dnsenum on {target}')
    os.system(command)

def run_dnsmap(target, output_folder):
    output_file = os.path.join(output_folder, 'dnsmap', f'{target}_dnsmap.txt')
    command = f'dnsmap {target} -w subdomains.txt -r {output_file}'
    print(f'[INFO] Running dnsmap on {target}')
    os.system(command)

def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f'[INFO] Created output directory: {output_folder}')

    # Create subdirectories for each DNS tool
    tools = ['dnsrecon', 'dnsenum', 'dnsmap', 'dig', 'whois', 'nslookup']
    for tool in tools:
        tool_folder = os.path.join(output_folder, tool)
        if not os.path.exists(tool_folder):
            os.makedirs(tool_folder)
            print(f'[INFO] Created output directory: {tool_folder}')

def run_other_dns_tools(target, output_folder):
    # Create output file names in their respective folders
    dig_output = os.path.join(output_folder, 'dig', f'{target}_dig.txt')
    whois_output = os.path.join(output_folder, 'whois', f'{target}_whois.txt')
    nslookup_output = os.path.join(output_folder, 'nslookup', f'{target}_nslookup.txt')

    # Run dig
    print(f'[INFO] Running dig on {target}')
    os.system(f'dig {target} > {dig_output}')

    # Run whois
    print(f'[INFO] Running whois on {target}')
    os.system(f'whois {target} > {whois_output}')

    # Run nslookup
    print(f'[INFO] Running nslookup on {target}')
    os.system(f'nslookup {target} > {nslookup_output}')

def worker(target, output_folder):
    run_other_dns_tools(target, output_folder)
    run_dnsrecon(target, output_folder)
    run_dnsenum(target, output_folder)
    run_dnsmap(target, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run DNS enumeration tools on specified targets.')
    parser.add_argument('-i', '--input', type=str, required=True, help='File containing list of target domains')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder for results')
    parser.add_argument('--threads', type=int, default=100, help='Number of concurrent threads (default: 100)')

    args = parser.parse_args()

    target_file = args.input
    output_folder = args.output
    num_threads = args.threads
    
    create_output_folder(output_folder)
    targets = read_targets(target_file)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(worker, target, output_folder): target for target in targets}
        
        for future in as_completed(futures):
            target = futures[future]
            try:
                future.result()  # Wait for the worker to finish
                print(f'[INFO] Completed tasks for {target}')
            except Exception as e:
                print(f'[ERROR] An error occurred for {target}: {e}')

    print('[INFO] All DNS tasks completed.')


# how to run
# python script.py -i targets.txt -o dns_results --threads 50

