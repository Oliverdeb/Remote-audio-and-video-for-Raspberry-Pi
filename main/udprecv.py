import socket
import struct
import time
import webbrowser
import platform
import os
import subprocess

def get_ip_via_udp():
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	# open udp socket
	# socket code from python 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((MCAST_GRP, MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
	                             		# to MCAST_GRP, not all groups on MCAST_PORT
	mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	print("Waiting for UDP multicast from Raspberry Pi...")
	data, addr =  (sock.recvfrom(10240))
	print("Found Pi on ",addr[0])
	sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton('0.0.0.0'))
	sock.close()

	return (addr[0])

def start_stream():
	ip = get_raspi_IP()
	url = "https://" + ip + ":8080/stream/webrtc"
	print("Opening stream in browser at",url,'\nPLEASE ACCEPT THE CERTIFICATE')
	webbrowser.open(url, new=2,autoraise=True)

def set_static_ip():
	interfaces = ['eth0', 'wlan0']
	interface = ""
	while interface not in interfaces:
		interface = input("Specify the interface to set the static IP for ( wlan0 / eth0 ):\n: ")
	static_ip, subnet = input("Enter the static IPv4 address in the format xxx.xxx.xxx.xxx/yy where yy is the subnet mask.\ne.g 192.168.0.1/24\n: ").split('/')

	pi_ip = get_raspi_IP()
	print("about to ssh to set static ip of", static_ip, "on Raspi using ip of",pi_ip)
	if os.system("ssh pi@" + pi_ip + " sudo ip address add " + static_ip + "/" + subnet  + " dev " + interface) == 0:
		print("Successfully added static IP, storing in a text file. The static IP will be lost when the Pi reboots.")
		file = open("static_ip.txt", 'w')
		file.write(static_ip)
		file.close()
	else:
		print("Error assigning static IP.")
	main()

def get_raspi_IP():
	found, previous_static_ip = True, ""
	try:
		file = open("static_ip.txt", 'r')
		previous_static_ip = file.readline()
		if previous_static_ip == "":
			found = False
		# print("Got prev static IP", previous_static_ip,"was it",sep="")
	except:
		found = False
	if found and pingable(previous_static_ip):
		print("Using",previous_static_ip," as IP")
		return previous_static_ip
	if found:
		print("Could not ping pi on static IP of",previous_static_ip,"\nTrying avahi daemon ( raspberrypi.local ).")
	if pingable("raspberrypii.local"):
		print("Using raspberrypi.local as IP")
		return "raspberrypi.local"
	print("Could not ping pi on raspberrypi.local, trying UDP mutlicast")
	return get_ip_via_udp()

def pingable(ip):
	print("Trying to ping", ip)
	ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"	
	return((subprocess.run("ping " + ping_str + " -w 2 " + ip, shell=True)).returncode == 0)

def main():
	choice = eval(input("1) Set static IP for raspi\n2) Start start_stream\n3) Reset / delete previous static IP entry\n: "))
	if choice == 1:
		set_static_ip()
	elif choice == 2:
		start_stream()
	elif choice == 3:
		file = open("static_ip.txt",'w')
		file.write("")
		file.close()
	main()

if __name__ == "__main__":
	main()