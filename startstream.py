import socket
import struct
import time
import webbrowser
import platform
import os
import subprocess

def get_ip_via_udp():
	""" Returns the IP of the Raspberry Pi once a UDP multicast has been received from it. """
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	# open udp socket
	# socket code from python wiki: https://wiki.python.org/moin/UdpCommunication
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((MCAST_GRP, MCAST_PORT))  
	mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	print("Waiting for UDP multicast from Raspberry Pi...")
	data, addr =  (sock.recvfrom(10240))
	print("Multicast received from",addr[0])
	sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton('0.0.0.0'))
	sock.close()

	return (addr[0])

def start_stream():
	""" opens the stream url in a browser """
	ip = get_raspi_IP()
	url = "https://" + ip + ":8080/stream/webrtc"
	print("Opening stream in browser at",url,'\nPlease accept the self-signed ceritficate to view the stream.')
	webbrowser.open(url, new=2,autoraise=True)

def set_static_ip():
	""" sets a static IPv4 address for the specified interface using ssh."""
	interfaces = ['eth0', 'wlan0']
	interface = ""
	while interface not in interfaces:
		interface = input("Specify the interface to set the static IP for ( wlan0 / eth0 ):\n: ")
	static_ip, subnet = input("Enter the static IPv4 address in the format xxx.xxx.xxx.xxx/yy where yy is the subnet mask.\ne.g 192.168.0.1/24\n: ").split('/')

	pi_ip = get_raspi_IP()
	print("Trying to set static ip of", static_ip, "on Raspi using ip of",pi_ip,"over ssh.")

	# if command executed successfully then write it to a textfile.
	if os.system("ssh pi@" + pi_ip + " python /home/pi/set_static_ip.py " + static_ip + "/" + subnet + "#" + interface) == 0:
		print("Successfully added ", static_ip, " to ",interface," on the Raspberry Pi.", sep="")
		file = open("static_ip.txt", 'w')
		file.write(static_ip+"/"+subnet+"#"+interface)
		file.close()
	else:
		print("Error SSH'ing, couldn't set static IP.\nPlease try again")
	main()

def get_raspi_IP():
	""" get the IPv4 address associated with the Raspberry Pi """
	found, previous_static_ip = True, ""
	try:
		file = open("static_ip.txt", 'r')
		ipseg, interface = file.readline().split("#")
		previous_static_ip = ipseg.split("/")[0]
		found = previous_static_ip != ""
	except:
		found = False
	# First attempt. if pi is still accessible on the static IP found in the text file, use it.
	if found and pingable(previous_static_ip):
		print("Using",previous_static_ip, "as IP")
		return previous_static_ip
	# Second attempt. avahi-daemon
	if found:
		print("Could not ping pi on static IP of",previous_static_ip,"\nTrying avahi daemon ( raspberrypi.local ).")
	if pingable("raspberrypi.local"):
		print("Using raspberrypi.local as IP")
		return "raspberrypi.local"
	print("Could not ping pi on raspberrypi.local, waiting for UDP multicast")

	# Third attempt. If the first two failed, rely on the UDP multicasts to get the IP.
	return get_ip_via_udp()

def pingable(ip):
	print("Trying to ping", ip)
	ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"	
	return((subprocess.run("ping " + ping_str + " -w 2 " + ip, shell=True)).returncode == 0)

def remove_static_entry():
	try:
		file = open("static_ip.txt", "r")

		data = file.read()
		found = data != ""			
		os.system("rm static_ip.txt")
	except:
		found = False
	if not found:
		print("No static entry found.")
		return
	pi_ip = get_raspi_IP()
	os.system("ssh pi@" + pi_ip + " rm /home/pi/static_ip.txt")
	print("Previous static IP cleared.")

def main():
	choice = int(input("----------------------------------\n1) Set static IP for raspi\n2) Start stream\n3) Reset / delete previous static IP entry\n: "))
	if choice == 1:
		set_static_ip()
	elif choice == 2:
		start_stream()
	elif choice == 3:
		remove_static_entry()		
	main()

if __name__ == "__main__":
	main()
