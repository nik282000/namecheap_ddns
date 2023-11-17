#!/usr/bin/env python3

import socket
import requests

'''
domain_list is a list of dicts containing a domain string, password string, and list of hosts for that domain
At least one host must be provided, @ is the root/bare domain, * for wildcards. Example below:
[{"domain" : "DOMAIN.TLD", "password" : "NamecheapPassword", "hosts" : ["@", "SUBDOMAIN"]}]
'''
domain_list = [
    {"domain" : "your.domain", "password" : "YourDDNSPassword", "hosts" : ["@", "*"]},
    {"domain" : "another.com", "password" : "ADifferentPassword", "hosts" : ["@", "yet"]}
    ]

debug = False


def debug_print(message):
    if debug:
        print(message)


# Check the current WAN IP address
def check_ip():
    try:
        return requests.get('http://dynamicdns.park-your-domain.com/getip').text
    except:
        print('Could not look up WAN IP. Aborting.')
        exit()


# Check the IP associated with a given host, log error and quit if IP check fails
def check_dns(domain, host): 
    if host[0] == "*":
        # Replace wildcard host with 'test' because you cant resolve *
        host = host.replace('*', 'test')
        hostname = host + '.' + domain
    # Check the bare domain
    elif host == '@':
        hostname = domain
    # Check normal hosts/subdomains
    else:
        hostname = host + '.' + domain
    try:
        return socket.gethostbyname(hostname)
    except:
        print(f'Could not look up host IP for {hostname}. Aborting.')
        exit()


# Parse the DDNS update response from park-your-domain.com, return the first error or 0 if everything was ok
def parse_response(response):
    response = response.split('\n')
    error = 0
    # Find the Err1 tags, remove them and return the message.
    for i in range(len(response)):
        if response[i].strip().find('<Err1>') > -1:
            error = response[i].strip()[6:-7]
    return error


# Build the webhook url and send it, return the parsed response or an error string
def update_dns(domain, host, password, ip):
    try:
        request_string = f'http://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}&ip={ip}'
        response = parse_response(requests.get(request_string).text)
        return response
    except:
        return(f'Could not update DNS for {host}.{domain}')


# Update my DDNS
wan_ip = check_ip()

'''
Itterate through Domains and Hosts listed for each domain
Check WAN ip against current Namecheap IP
If DNS IP != WAN IP then update the DDNS
Print any error responses
'''
for d in range(len(domain_list)):
    for h in range(len(domain_list[d]['hosts'])):
        debug_print(domain_list[d]['hosts'][h] + ' ' + domain_list[d]['domain'])
        host_ip = check_dns(domain_list[d]['domain'], domain_list[d]['hosts'][h])
        if host_ip != wan_ip:
            debug_print("DNS Out of date")
            response = update_dns(domain_list[d]['domain'], domain_list[d]['hosts'][h], domain_list[d]['password'], wan_ip)
            if response != 0:
                print(f"{domain_list[d]['hosts'][h]}.{domain_list[d]['domain']} {response}")
            else:
                print(f"{domain_list[d]['hosts'][h]}.{domain_list[d]['domain']} updated")
        else:
            print(f"{domain_list[d]['hosts'][h]}.{domain_list[d]['domain']} is up to date")
