# NetworksDB.io official Python library

This is the official Python client for the NetworksDB API. This allows you to lookup owner details for any IPv4 or IPv6 IP address, find out which networks, IP addresses and domains are operated by organisations, and much more.

**This requires a NetworksDB API token**. You can get one for free at our website, https://networksdb.io/api/docs. Free keys come with limitations, such as a limited monthly quota and truncated output for large result sets.

The details returned by the API include, but aren't limited to, the following:

- **Organisation info**: Name, address, phone, countries, number of IPv4 and IPv6 networks, number of networks by country, assigned ASNs
- **Organisation networks**: Description, name, size, CIDR, start IP, end IP for each network operated by a specific organisation
- **IP info**: Number of domains resolving to the IPv4 or IPv6 address, owner organisation info, name and description of the network containing the address.
- **IP geolocation**: Country, state, city, latitude and longitude. 
- **ASN info**: Information about the autonomous system, including the owner company.
- **ASN networks**: IPv4/6 network prefixes announced by the autonomous system, including the company they are allocated to.
- **Reverse DNS**: List of domain names resolving to the IP address.
- **"Mass" reverse DNS**: List of domain names resolving to addresses in an IP range *(not available to free API keys)*.

## Installation

```
pip install networksdb
```

Or clone the repository and run `python3 setup.py install`.

## Quick Start

Start by getting an instance of a NetworksDB API handler, supplying your API key.
```
from networksdb import NetworksDB
>>> api = NetworksDB('11111111-2222-3333-4444-555555555555')
```
Get information about an IP address:
```
>>> ip = api.ip_info('8.8.8.8')
```
Omitting the parameter will return information about your source IP address.

Return information about the owner, networks and domains:
```
>>> ip.organisation.name
'Google LLC'
>>> ip.domains_on_ip
7243
>>> ip.network.cidr
'8.8.8.0/24'
>>> ip.network.netname
'LVLT-GOGL-8-8-8'
```

Request geolocation information (This works with IPv6 addresses too):
```
>>> geo = api.ip_geo('8.8.8.8')
>>> geo.continent, geo.country, geo.state, geo.city, geo.latitude, geo.longitude
('North America', 'United States', 'California', 'Mountain View', 37.406, -122.079)
```

View the full API response details by printing any `Response` object:
```
>>> print(ip)
{
    "ip": "8.8.8.8",
    "domains_on_ip": 7243,
    "url": "https://networksdb.io/ip/8.8.8.8",
    "organisation": {
        "name": "Google LLC",
        "id": "google-llc",
        "url": "https://networksdb.io/ip-addresses-of/google-llc"
    },
    "network": {
        "netname": "LVLT-GOGL-8-8-8",
        "description": "Google LLC",
        "cidr": "8.8.8.0/24",
        "first_ip": "8.8.8.0",
        "last_ip": "8.8.8.255",
        "url": "https://networksdb.io/ips-in-network/8.8.8.0/8.8.8.255"
    }
}
```

### Organisation search

To request organisation details, you need to supply its NetworksDB `id`. To find organisation IDs, use the *organisation search API*  The results are sorted by the number of IPv4 addresses for each organisation:

```
>>> search = api.org_search('Github')
>>> search.total
1
>>> search.results[0].organisation
'GitHub, Inc'
>>> search.results[0].id
'github-inc'
```

### Organisation info
Once you've found the correct ID, pass it to the *organisation info* API call:
```
>>> github = api.org_info('github-inc')
>>> print(github)
{
    "organisation": "GitHub, Inc",
    "id": "github-inc",
    "address": null,
    "phone": null,
    "countries": [
        "United States"
    ],
    "networks": {
        "ipv4": 8,
        "ipv6": 2
    },
    "networks_by_country": {
        "United States": 10
    },
    "url": "https://networksdb.io/ip-addresses-of/github-inc",
    "asns": [
        "36459"
    ]
}
```

### Organisation networks

Find out which networks they own or operate:
```
>>> github_networks = api.org_networks(github.id)
>>> for range in github_networks.results:
...     print(range.netname, range.description, range.cidr)
... 
GITHU GitHub, Inc 140.82.112.0/20
US-GITHUB-20170413 GitHub, Inc 185.199.108.0/22
GITHUB-NET4-1 GitHub, Inc 192.30.252.0/22
RSPC-728F4421-0D7C-4F42-BDFD-A6D290538501 GitHub 74.205.116.224/28
ZAYO-IDIA-235983-64-124-138-32-28 GitHub 64.124.138.32/28
RSPC-039EB5D8-39DC-445A-9C23-05529A657DDC GitHub 148.62.46.192/29
RSPC-48B1F3A4-2615-4566-99CD-D126E3C102BB GitHub 174.143.3.100/30
RSPC-CC4A7060-6141-4A22-BD6B-98A2B581247D GitHub 148.62.46.150/31
```
Or, for IPv6:
```
>>> github_ipv6_networks = api.org_networks(github.id, ipv6=True)
>>> for range in github_ipv6_networks.results:
...     print(range.netname, range.description, range.cidr)
... 
US-GITHUB-20170419 GitHub, Inc 2a0a:a440::/29
GITHUB-NET6-1 GitHub, Inc 2620:112:3000::/44
```

### Reverse DNS

List the domains names resolving to a given IPv4 or IPv6 address:
```
>>> reverse_dns = api.reverse_dns('185.199.108.153')
>>> reverse_dns.total
96658
>>> reverse_dns.results[:10]
('0-0.uk', '0000000000000.net', '000fff.design', '001.run', '0061.ru', '00ul.com', '01-partners.com', '01010111.com', '013627.xyz', '01coin.io')
```
Mass reverse DNS is the same thing, but on a full network block:
```
>>> mass_reverse = api.mass_reverse_dns('185.199.108.0/22')
>>> mass_reverse.total
359808
>>> for res in mass_reverse.results[:4]:
...     print(res.ip, res.domains)
... 
185.199.108.0 ('jidanlee.com', 'jitianbo.com', 'tessmichi.com')
185.199.108.1 ('deepwaves.tech',)
185.199.108.15 ('canyourecognize.ga', 'djuric.se', 'glenberis.co.uk', 'hectormanrique.com', 'trustkaro.com')
185.199.108.22 ('jidanlee.com',)
```
*Note: Mass reverse DNS is not available to free API keys.*

### Find all domains hosted by a company
It's pretty easy to iterate through the company's networks and request the list of domain names for each network:
```
>>> for network in api.org_networks('paypal-inc').results:
...     mass_reverse = api.mass_reverse_dns(network.first_ip, network.last_ip)
...     print([_.domains for _ in mass_reverse.results])
... 
[...]
[('test-paypal.com',), ('test-paypal.com',), ('paypal-australia.com.au', 'paypal-business.co.uk', 'paypal-business.com.au', 'paypal-businesscenter.com', 'paypal-communications.com', 'paypal-danmark.dk', 'paypal-donations.co.uk', 'paypal-donations.com', 'paypal-globalshops.com', 'paypal-knowledge-test.com', 'paypal-knowledge.com', 'paypal-marketing.ca', 'paypal-marketing.co.uk', 'paypal-media.com', 'paypal-norge.no', 'paypal-optimizer.com', 'paypal-partners.com', 'paypal-passport.com', 'paypal-prepagata.com', 'paypal-promo.es', 'paypal-sverige.se', 'paypal-turkiye.com', 'paypal.com.cn', 'paypalbenefits.com', 'paypalgivingfund.org', 'paypalobjects.com'), ('paypal-australia.com.au', 'paypal-business.co.uk', 'paypal-business.com.au', 'paypal-businesscenter.com', 'paypal-communications.com', 'paypal-danmark.dk', 'paypal-donations.co.uk')]
[...]
```

### ASN information
Request information about a particular ASN:
```
>>> asn = api.asn_info(19956)
>>> asn.as_name, asn.description, asn.networks_announced.ipv4
('TENNESSEE-NET', 'AT&T Corp.', 18)
```
Retreive the networks announced by the ASN and find out who they are assigned to (for IPv6, pass the parameter `ipv6=True`):
```
>>> as_nets = api.asn_networks(19956)
>>> for net in as_nets.results:
...     print(net.cidr, net.countrycode, net.organisation.name)
... 
12.204.201.0/24 US AT&T Services, Inc.
12.204.208.0/24 US State of Tennesse-Nettn
12.204.209.0/24 US AT&T Services, Inc.
64.79.176.0/21 US Southwest Tennessee Community College
64.79.184.0/21 US Southwest Tennessee Community College
66.4.14.0/23 US AT&T Services, Inc.
66.4.27.0/24 US AT&T Services, Inc.
66.4.28.0/22 US AT&T Services, Inc.
70.150.247.0/24 US TNII Networks
72.159.76.0/24 US Tennessee State Govt
170.141.60.0/23 US AT&T Services, Inc.
170.141.62.0/24 US AT&T Services, Inc.
170.178.136.0/22 US Motlow State Community College
192.230.240.0/20 US Chattanooga State Community College
198.146.0.0/16 US Tennessee Board of Regents
206.23.0.0/16 US Tennessee Board of Regents
208.63.129.0/24 US AT&T Services, Inc.
208.182.101.0/24 US AT&T Services, Inc.
```