import os

print(os.system("ssh pi@raspberrypi.local sudo ip address add 172.21.0.234/24 dev wlan0;exit"))