#!/usr/bin/python3

import json
import sys, os, operator

#CAN BE CHANGED BUT MUST MATCH TB SOURCE CODE
KEY = 'Q'

class EncodeString(object):
	def __init__(self, url=None):
		self.raw = []

		if url is not None:
			self.add(url)

	def add(self, clearText):
		for a in range(0,len(clearText)):
			c = ord(clearText[a])
			k = ord(KEY)
			self.raw.append(str(operator.xor(c, k) % 255))

	def __str__(self):
		return "{%s}"%(",".join(self.raw))

def make_header(configuration):
	with open("auto_config.h", "w") as f:
		for key in configuration.keys():
			f.write("#define {} {}\n".format(key,configuration.get(key)))

if __name__ == "__main__":
	with open("configuration.json", "r") as configuration_file:
		configuration = json.load(configuration_file)

	header_configuration = {
		"_DNSARRAY": 0,
		"_DNSCODESIZE": 0,
		"_DNSCODE": "",
        "_ERRORTIMEOUT": str(configuration.get("error_timeout"))
	}

	_DNSCODE = []
	for url in configuration["callback"]:
		es = EncodeString(url)
		es.raw.append(str(-1))
		
		_DNSCODE.append(str(es))
		header_configuration["_DNSARRAY"] += 1
        
		#calculate max url size
		if len(str(es)) > header_configuration["_DNSCODESIZE"]:
			header_configuration["_DNSCODESIZE"] = len(str(es)) + 2

	header_configuration["_DNSCODE"] = "{ %s }"%", ".join(_DNSCODE)

	make_header(header_configuration)

	print("Generated auto_config.h")