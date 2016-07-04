# About this project

This project was completed during a 4-week internship. 

# Aim

To serve and receive audio and video simultaneously from a Raspberry Pi using the Raspberry Pi camera module and a USB headset attached to the Pi.

# Gotcha

This implementation only works over LAN. Using services like [weaved](https://www.weaved.com/) or port-forwarding will get you going for internet streaming too - but beware *it is very bandwidth intensive*. You will have to play around with the fps and quality a fair amount to get a stable stream ( bandwidth dependent. )

## Prerequisites:
  * Python 2.7 for *UDPcast.py* on the Raspberry Pi.
  * Python 3.5 for the stream-client/Raspberry Pi IP finder on the client.
  * UV4L installed on the Raspberry Pi ( see below for installation details. )
  * avahi-daemon installed on Raspberry Pi ( not mandatory, but can make things easier, used to automatically resolve raspberrypi.local to its IPv4 address. )
  * Camera module / webcam for video and a headset with a microphone for the Raspberry Pi.(*obviously*).
  * Raspbian Jessie / Wheezy installed on the Raspberry Pi.
  * SSH needs to be enabled on the Raspberry Pi for a static IP to be set using 

## Steps:
  1. See this guide to install and set up UV4L on the Raspberry Pi.( *HTTPS is mandatory if you want WebRTC to work, which is needed for two-way audio/video.* You can however stream video from the Raspberry Pi over HTTP with no problems. 
  2. I had to manually edit */etc/asound.conf* to change the priority of the USB audio to be a higher priority than the onboard audio card.
   
   ''''sudo nano /etc/asound.conf'
   ```python
   s = "Python syntax highlighting"
   print s
   ```
  3. Add the UDPCast.py script to xxx to launch on startup on the Raspberry Pi.
  4. 
