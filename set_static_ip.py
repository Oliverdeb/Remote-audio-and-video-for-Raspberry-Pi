import sys
import os

ipseg, interface = sys.argv[1].split("#")

file = open("/home/pi/static_ip.txt", 'w')
file.write(sys.argv[1])
file.close()

os.system("sudo ip address add " + ipseg + " dev " + interface )
