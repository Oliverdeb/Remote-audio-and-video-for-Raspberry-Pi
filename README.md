## About this project

This project was completed during a 4-week internship. 

## Aim

To send and receive audio and video simultaneously from a Raspberry Pi using the Raspberry Pi camera module and a USB headset attached to the Pi ( all done by UV4L ). I was to implement a way to start the stream without knowing the IP of the Raspberry Pi before hand. 

## Gotcha

This implementation only works over LAN. Using services like [weaved](https://www.weaved.com/) or port-forwarding will get you going for internet streaming too - but beware *it is very bandwidth intensive*. You will have to play around with the fps and quality a fair amount to get a stable stream ( bandwidth dependent ).

## Prerequisites:
  * Python 2.7 for *UDPmulticaster.py* on the Raspberry Pi.
  * Python 3.5 for the *startstream.py* script on the client.
  * UV4L installed on the Raspberry Pi ( see below for installation details ).
  * avahi-daemon installed on Raspberry Pi ( not mandatory, but can make things easier, used to automatically resolve raspberrypi.local to its IPv4 address ).
  * Camera module / webcam for video and a headset with a microphone for the Raspberry Pi.
  * Raspbian Jessie / Wheezy installed on the Raspberry Pi.
  * A power source of some kind, this is intended to be portable ( PoE / a power bank capable of > 2A output ).
  * SSH needs to be enabled on the Raspberry Pi for a static IP to be set using *startstream.py*.

## Steps:
  1. See [this guide](http://www.linux-projects.org/uv4l/installation/) to install and set up UV4L on the Raspberry Pi. ( *HTTPS is mandatory if you want WebRTC to work, which is needed for two-way audio/video.* You can however stream video from the Raspberry Pi over HTTP with no problems ).
  
  2. Edit the UV4L config at  */etc/uv4l/uv4l-raspicam.conf*  to configure the driver, core module and server paramaters. *(This config is run by UV4L at start-up. Therefore the HTTPS certificates and private keys etc must be set here if you want the UV4L server to start-up automatically the way you want it configured).*
  3. Edit  /*etc/modprobe.d/alsa-base.conf*  to change the priority of the USB audio to be a higher priority than the onboard audio card.
   
   ```shell
   options snd-usb-audio index=0
   options snd_bcm2835 index=1
   ```
  4. Add the following line to  */etc/rc.local*  to launch UDPmulticaster.py on Raspberry Pi startup.
  
   ```shell
   python /yourpath/UDPmulticaster.py &
   ```
   
   **Replace yourpath** with the path to the script. (**Ensure** UDPmulticaster.py has execute permissions,
   run the following if you are unsure).
   
   ```shell
   sudo chmod u+x /yourpath/UDPmulticaster.py 
   ```
   
   This will just make it easier to stream to the Raspberry Pi as you won't have to know the IP of the Raspberry Pi beforehand, you can alternatively just set a static IP if you have router access.
  5. Reboot and your Pi should be accessible by using the *startstream.py* script. 
 
    ```shell
   python startstream.py
   ```
  Simply follow the on-screen menu to start the stream or set a static IP ( **Not permanent, the Pi will not retain the IP on power loss** *This just allows the Pi to listen on more than one IPv4 address. Therefore allowing you to set and know the IP address before-hand. i.e. you can set an IP to listen on before you even connect to a network and once you do connect to it the Pi will listen on a pre-set IPv4 address, allowing you to connect to it and stream from the pre-set IP.* ).
