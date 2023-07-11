import requests
import json

class Response(dict):

	def __getattr__(self, key):
		if key in self:
			return Response(self[key]) if isinstance(self[key], dict) else self[key]

		raise AttributeError(f"'Response' object has no attribute '{key}'")

	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__

	def __str__(self):
		return json.dumps(self, indent=4)

class NetworksDB(object):

	def __init__(self, apikey=None):
		self.apikey = apikey
		self.endpoint = 'https://networksdb.io'

	def request(self, path, params={}):
		res = requests.post('{}{}'.format(self.endpoint, path), headers={'X-Api-Key': self.apikey}, data=params).json()
		return Response(res)

	def key_info(self):
		return self.request('/api/key')

	def ip_info(self, ip=None):
		if ip:
			return self.request('/api/ip-info', {'ip': ip})
		else:
			return self.request('/api/ip-info') # Will return info for your own IP

	def ip_geo(self, ip=None):
		if ip:
			return self.request('/api/ip-geo', {'ip': ip})
		else:
			return self.request('/api/ip-geo') # Will return info for your own IP

	def org_search(self, query):
		return self.request('/api/org-search', {'search': query})

	def org_info(self, id):
		return self.request('/api/org-info', {'id': id})

	def org_networks(self, id, ipv6=False):
		if ipv6:
			return self.request('/api/org-networks', {'id': id, 'ipv6': True})
		else:
			return self.request('/api/org-networks', {'id': id})

	def asn_info(self, asn):
		return self.request('/api/asn-info', {'asn': asn})

	def asn_networks(self, asn, ipv6=False):
		if ipv6:
			return self.request('/api/asn-networks', {'asn': asn, 'ipv6': True})
		else:
			return self.request('/api/asn-networks', {'asn': asn})

	def dns(self, domain):
		return self.request('/api/dns', {'domain': domain})

	def reverse_dns(self, ip):
		return self.request('/api/reverse-dns', {'ip': ip})

	def mass_reverse_dns(self, start, end=None):
		if end:
			return self.request('/api/mass-reverse-dns', {'ip_start': start, 'ip_end': end})
		else:
			return self.request('/api/mass-reverse-dns', {'cidr': start})
