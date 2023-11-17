A python script to update DDNS entries with NameCheap.

Your domains to be updated are stored in a list of dictionaries with each dict containing your domain, ddns password and a list of subdomains.
At least one subdomain must be listed, usually @ which is the bare/root domain. Specific subdomains and/or wildcards can be added as well.

Example:
[

{"domain" : "domain.tld", "password" : "NamecheapPassword", "hosts" : ["@", "*"]}

{"domain" : "other.com", "password" : "DifferntNamecheapPassword", "hosts" : ["subdomain", "*.subdomain"]},

]

The above will update the DDNS for domain.tld, *.domain.tld, subdomain.other.com, and *.subdomain.other.com
