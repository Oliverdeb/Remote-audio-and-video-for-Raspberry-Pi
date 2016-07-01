import tkinter as tk
import webbrowser as web
import os, platform

# Ping from raspi to static IP of user
# arp -a on user to get Raspi IP
# initiate remote view on found IP


class simpleapp_tk(tk.Tk):
	url = "https://raspberrypi.local:8080/stream/webrtc"
	ip = "raspberrypi.local"
	def __init__(self,parent):
        	tk.Tk.__init__(self,parent)
        	self.parent = parent
        	self.minsize(width=640, height=480)
        	self.resizable(width=False, height=False)
        	self.initialize()

	def initialize(self):
		self.grid()

		main_label = tk.Label(self, text="Raspberry Pi remote viewer")
		# main_label.grid(column=0,row=0)
		main_label.config(anchor=tk.CENTER)
		main_label.pack()
		self.entry = tk.Entry(self)
		# self.entry.grid(column=0,row=1) # East West, i.e stick to left right on resize
		self.entry.pack()
		self.entry.insert(0,self.url)
		self.entry.config(state=tk.DISABLED)
		# self.entry.pack(expand=1, fill=tk.X)
		self.entry.config(width=50)

		availibility_label = tk.Label(self, text="Checking Pi status...")
		availibility_label.config(anchor=tk.CENTER)
		availibility_label.pack()

		button = tk.Button(self,text="Go to remote view", command=self.start)
		button.config(state=tk.DISABLED)
		# button.grid(column=1,row=0)
		button.pack()
		if self.check_status(self.ip):
			availibility_label.config(text= "Pi is online @ " + self.ip)
			button.config(state=tk.NORMAL)
		else:
			availibility_label.config(text= "Could not contact Raspberry Pi at " + self.ip)
			pi_finder_button = tk.Button(self, text="Start Adafruit's Raspi local IP finder..", command=self.pifinder)
			pi_finder_button.pack()
			self.entry.config(state=tk.NORMAL)


	def pifinder(self):
		os.system("../pibootstrap/./pibootstrap")

	def start(self):		
		web.open_new(self.url)


	def check_status(self, host):
		# This code is from the below url:
		# http://stackoverflow.com/questions/2953462/pinging-servers-in-python

	    # Ping parameters as function of OS
	    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

	    # Ping
	    # print()
	    return os.system("ping " + ping_str + " -w 2 " + host) == 0
		# print(os.system("ping -c 1 -w2 " + host ))
		# return os.system("ping -c 1 -w2" + host + " > /dev/null 2>&1") == 0
	
if __name__ == "__main__":
    	app = simpleapp_tk(None)
    	app.title('Remote view for Raspi')
    	app.mainloop()

