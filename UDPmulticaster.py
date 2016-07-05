#!/usr/bin/env python

import subprocess
import socket
import time
import re

def main():
	
	# keep looping until Raspi has been allocated an IPv4 address
	while True:
		while not has_ipv4_address():	
			time.sleep(10)
		multicast()

def multicast():	
	""" UDP multicasts every 5 seconds to the multicast group while there is a valid IPv4 address. """
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	# mutlicast every 5 seonds while there is a valip IP.
	while has_ipv4_address():
		sock.sendto("Alive", (MCAST_GRP, MCAST_PORT))
		time.sleep(5)

def has_ipv4_address():
	""" This function checks to see if the Raspi has been allocated an IPv4 address"""

	# list of network interfaces on the Raspi to check for an ipv4 address.
	cmds = [
		"ifconfig eth0 | grep \"inet addr\"",
		"ifconfig wlan0 | grep \"inet addr\""
		]

	#map over the list of cmds passing each cmd to be executed in the shell, then loop over the list of results.
	for result in map(lambda x: shell(x), cmds):
		# the following regex checks to see a valid ipv4 address follows after addr. e.g inet addr:192.168.1.1
		if re.search(r"addr\:(\d{1,3}\.){3}(\d{1,3})", str(result)):
			return True			
	return False

def shell(cmd):	
	""" Executes a given shell command and returns the output """
	return (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)).communicate()[0]

if __name__ == "__main__":
	main()
