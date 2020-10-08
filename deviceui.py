try:
	from ppadb.client import Client as AdbClient
except:
	from adb.client import Client as AdbClient
import sys
from random import randint
import datetime
import time
import re
import os
from bs4 import BeautifulSoup


class Device:
	def __init__(self,deviceid,app="instagram",wirelessip=None,Pt=None):

		apps = {
			"instagram" : "com.instagram.android/com.instagram.android.activity.MainTabActivity",
			"tiktok" : "com.ss.android.ugc.trill/com.ss.android.ugc.aweme.splash.SplashActivity",
			"linkedin" : "com.linkedin.android.salesnavigator/com.linkedin.android.salesnavigator.ui.home.HomeV2Activity"
		}

		self.app = apps[app]
		self.mainapp_name = apps[app].split('/')[0]

		client = AdbClient(host="127.0.0.1", port=5037)
		self.device = client.device(deviceid)
		self.deviceid = deviceid

		if not os.path.isdir(deviceid):
			os.mkdir(deviceid)
		
		self.Pt = Pt

	def Printhis(self,message,color='default',**kwargs):
		if self.Pt is not None:
			self.Pt(message,color,**kwargs)

	#################################################
	# GETTING DATA FROM DEVICE                      #################################################################################################################################
	#################################################

	def DumpData(self):
		check_dumpdata_try = 0 # Variable use to check how many times DumpData has tried
		idleerror = 0
		while True:
			if idleerror == 20:
				self.Printhis(message="Please Try Restarting your device before continuing",color="red")
				return False
			devicexml = self.device.shell("uiautomator dump", timeout=60)
			if check_dumpdata_try == 5:
				self.Printhis(message="Failed to get page data. Skipping Action",color="log")
				return False
			if "ERROR" in devicexml:
				devicexml = devicexml.strip('\n')
				if "idle" in devicexml:
					# IDLE state comment out to avoid # printing
					self.Printhis(message=f"{devicexml}",color="log")
					idleerror += 1
				else:
					self.Printhis(message=f"{devicexml}",color="log")
					check_dumpdata_try += 1
			else:
				return True

	def GetData(self,check=True,charlimit=8000):
		
		if check is False:
			if self.DumpData() is False:
				self.Printhis(message="Data Returning False from getdata | with check false",color='log')
				self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color='yellow')
				sys.exit(0)
			self.device.pull('/sdcard/window_dump.xml', self.deviceid + '/data.xml')
			with open(self.deviceid + '/data.xml', 'r', encoding="UTF-8") as data:
				data = data.read().encode(encoding="UTF-8")
			return data

		data = 'None'
		error = 0
		while len(data) < charlimit:
			if self.DumpData() is False:
				self.Printhis(message="Data Returning False from getdata | with check true",color="log")
				self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color="yellow")
				sys.exit(0)
			self.device.pull('/sdcard/window_dump.xml', self.deviceid + '/data.xml')
			with open(self.deviceid + '/data.xml', 'r', encoding="UTF-8") as data:
				data = data.read().encode(encoding="UTF-8")
			if error != 0:
				sys.stdout.write(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: Trying to getdata {error}/{15}\r')
				sys.stdout.flush()
				time.sleep(3)
			error += 1
			if error == 15:
				sys.stdout.write(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: Trying to getdata {error}/{15}\r')
				sys.stdout.flush()
				self.Printhis(message='Please check your network connection',color='red')
				sys.exit(0)

		return data


	############################################
	# BEGINING OF CONTROLS                     #################################################################################################################################
	############################################

	###############
	# RESOURCE ID #####################
	###############

	def Resourceid(self,id, hold=False, sec=5000, check=False, checkandclick=False, sleep=0.5, data='None',margin=(0,0,0,0)):

		if data == 'None':
			data = self.GetData()
			time.sleep(sleep)

		if check == True:
			try:
				x = BeautifulSoup(data,"html.parser").find(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
				minx, miny, maxx, maxy = x

				minx = int(minx) + margin[0]
				miny = int(miny) + margin[1]
				maxx = int(maxx) - margin[2]
				maxy = int(maxy) - margin[3]

				if checkandclick is True:
					self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
				return True
			except TypeError:
				return False

		x = BeautifulSoup(data,"html.parser").find(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
		minx, miny, maxx, maxy = x

		minx = int(minx) + margin[0]
		miny = int(miny) + margin[1]
		maxx = int(maxx) - margin[2]
		maxy = int(maxy) - margin[3]

		if hold == True:
			self.device.input_swipe(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)), randint(int(minx), int(maxx)),randint(int(miny), int(maxy)), sec)
			return True

		self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
		return True

	###########
	# TEXT ID #####################
	###########

	def Textid(self,id, hold=False, sec=5000, check=False, checkandclick=False, resourceid='None', sleep=0.5, data='None',margin=(0,0,0,0)):
		
		if data == 'None':
			data = self.GetData()
			time.sleep(sleep)

		if resourceid != 'None':
			x = BeautifulSoup(data,"html.parser").find(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{resourceid}$',re.I),"text":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
			minx, miny, maxx, maxy = x

			minx = int(minx) + margin[0]
			miny = int(miny) + margin[1]
			maxx = int(maxx) - margin[2]
			maxy = int(maxy) - margin[3]

			self.device.input_tap(randint(int(minx) , int(maxx)), randint(int(miny), int(maxy)))
			return True

		if check == True:
			try:
				x = BeautifulSoup(data,'html.parser').find(attrs={"text":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
				minx, miny, maxx, maxy = x

				minx = int(minx) + margin[0]
				miny = int(miny) + margin[1]
				maxx = int(maxx) - margin[2]
				maxy = int(maxy) - margin[3]

				if checkandclick is True:
					self.device.input_tap(randint(int(minx) , int(maxx)), randint(int(miny), int(maxy) ))
				return True
			except TypeError:
				return False

		x = BeautifulSoup(data,'html.parser').find(attrs={"text":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
		minx, miny, maxx, maxy = x

		minx = int(minx) + margin[0]
		miny = int(miny) + margin[1]
		maxx = int(maxx) - margin[2]
		maxy = int(maxy) - margin[3]

		if hold == True:
			self.device.input_swipe(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)), randint(int(minx), int(maxx)),randint(int(miny), int(maxy)), sec)
			return True

		self.device.input_tap(randint(int(minx) , int(maxx) ), randint(int(miny), int(maxy)))
		return True



	##############
	# CONTENT ID #####################
	##############

	def Contentid(self,id, hold=False, sec=5000, check=False, checkandclick=False, resourceid='None', sleep=0.5, data='None', margin=(0,0,0,0)):
		
		resourceid = resourceid
		if data == 'None':
			data = self.GetData()
			time.sleep(sleep)
		if resourceid != 'None':
			x = BeautifulSoup(data,"html.parser").find(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{resourceid}$',re.I),"content-desc":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
			minx, miny, maxx, maxy = x

			minx = int(minx) + margin[0]
			miny = int(miny) + margin[1]
			maxx = int(maxx) - margin[2]
			maxy = int(maxy) - margin[3]

			self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
			return True


		if check == True:
			try:
				x = BeautifulSoup(data,'html.parser').find(attrs={"content-desc":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
				minx, miny, maxx, maxy = x

				minx = int(minx) + margin[0]
				miny = int(miny) + margin[1]
				maxx = int(maxx) - margin[2]
				maxy = int(maxy) - margin[3]

				if checkandclick is True:
					self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
				return True
			except TypeError:
				return False

		x = BeautifulSoup(data,'html.parser').find(attrs={"content-desc":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
		minx, miny, maxx, maxy = x

		minx = int(minx) + margin[0]
		miny = int(miny) + margin[1]
		maxx = int(maxx) - margin[2]
		maxy = int(maxy) - margin[3]

		if hold == True:
			self.device.input_swipe(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)), randint(int(minx), int(maxx)),randint(int(miny), int(maxy)), sec)
			return True

		self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
		return True


	######################################################
	# MISC OF CONTROLS                                   #################################################################################################################################
	######################################################

	###############
	# OPENING APP #####################
	###############


	def OpenApp(self):
		self.device.shell(f"am start -n {self.app}")

	###############
	# CLOSE APP #####################
	###############		

	def CloseApp(self):
		self.device.shell(f"am force-stop {self.mainapp_name}")

	#################
	# OPEN VIA LINK #####################
	#################

	def OpenLink(self,link):
		self.device.shell(f'am start -a "android.intent.action.VIEW" -d "{link}"')

	###########################
	# WRITING TEXT WITH SPACE #####################
	###########################

	def WriteText(self,text):

		text = text.replace("\\","\\\\")
		text = text.replace("$","\$")
		text = text.replace(" ","%s")
		self.device.input_text(text)


	####################
	# PAGE LOAD CHECKS #####################
	####################

	def PageLoadCheck(self,mustexist,ui="text",shouldcontinue=False,retry=60):
		""" mustexist takes lists """
		pagecheckererror = 1
		while True:
			self.Printhis(f"Waiting for page to load",'vanish')
			pdata = self.GetData(check=False)
			for words in mustexist:
				if ui == "text":
					if self.Textid(words,check=True,data=pdata) is True:
						return True
				if ui == "resource-id":
					if self.Resourceid(words,check=True,data=pdata) is True:
						return True
				if ui == "content-desc":
					if self.Contentid(words,check=True,data=pdata) is True:
						return True
			if pagecheckererror == retry:
				if shouldcontinue is False:
					self.Printhis(message='Page did not load correctly. Restarting Bot...'.ljust(20),color="vanish")
					self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color="yellow")
					self.Printhis(message='Exception Raised Because PageLoadCheck Failed',color='log')
					sys.exit(0)
				if shouldcontinue is True:
					return False
			pagecheckererror += 1
			time.sleep(1)


	#####################
	# GET UI TEXT VALUE #####################
	#####################


	def UInteract(self,outputid,inputid,inputvalue,all=False,data='None',mute=False):
		outputid = outputid
		inputid = inputid
		inputvalue = inputvalue
		if data == 'None':
			data = self.GetData()

		if outputid == 'text' and inputid == 'resource-id':
			# Mute is used for MUTEFEED Method for Muting
			if mute is True:
				x = re.findall(r'text="([\d|\,|\.|\w|\s]{1,})\?" resource-id="'+self.mainapp_name+':id/' + inputvalue + '"',str(data), flags=re.IGNORECASE)
			else:
				x = re.findall(r'text="([\d|\,|\.|\w|\s]{1,})" resource-id="'+self.mainapp_name+':id/' + inputvalue + '"',str(data), flags=re.IGNORECASE)
			if all is False:
				x = str(x[0])
			return x

		if outputid == 'checked' and inputid == 'resource-id':
			x = re.findall(r'resource-id="'+self.mainapp_name+':id/' + inputvalue + '" .*? checked="(\w{1,5})"',str(data), flags=re.IGNORECASE)
			if all is False:
				x = str(x[0])
			return x

	################
	# SWIPE SCREEN #####################
	################

	def SwipeScreen(self,method,times=1):
		if method == "scrolldown":
			for _ in range(times):
				self.Printhis(message=f"Scrolling Down          ",color="vanish")
				self.device.input_swipe(randint(197, 428), randint(748, 763), randint(197, 428), randint(548, 563), 500)	
		elif method == "scrollup":
			for _ in range(times):
				self.Printhis(message=f"Scrolling Up          ",color="vanish")
				self.device.input_swipe(randint(197, 428), randint(548, 563), randint(197, 428), randint(748, 763), 500)
		else:
			start_x, start_y, end_x, end_y = method
			self.device.input_swipe(start_x, start_y, end_x, end_y, 500)

	##################
	# GET CURRENT UI #####################
	##################

	def Snapshot(self,foldername='snapshot',filename=datetime.datetime.now().date()):

		if not os.path.isdir(f'{self.deviceid}/{foldername}'):
			os.mkdir(f'{self.deviceid}/{foldername}')
		self.device.shell('screencap -p /sdcard/screen.png')
		self.device.shell('uiautomator dump')
		self.device.pull('/sdcard/screen.png',f'{self.deviceid}/{foldername}/{filename}.png')
		self.device.pull('/sdcard/window_dump.xml',f'{self.deviceid}/{foldername}/{filename}.uix')
		return True

	#####################
	# GET CURRENT FOCUS #####################
	#####################

	def GetCurrentFocus(self):
		return self.device.shell("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")

	#############################
	# CHECK INTERNET CONENCTION #####################
	#############################

	def IsConnectedToInternet(self):

		"""
			Check Internet or mobile data connection.
			Will return True if a connection is establish and
			False if there's no internet or data connection
		"""


		ping_response = self.device.shell('ping -c 1 google.com')
		if 'unknown host' in ping_response:
			return False
		else:
			return True

	def ContinueOnlyIfInternet(self,retry=None):

		"""
			Function to continue only if there's internet or mobile data connection.
			Function will loop forever if connection is not establish so becareful
		"""


		while True:
			if self.IsConnectedToInternet() is True:
				return True
			else:
				# print('sleeping')

				if retry is not None:
					error =+ 1
					if error == retry:
						return False

				time.sleep(10)

		return True

	#############################
	# CHECK DEVICE WAKE STATE #####################
	#############################

	def DeviceWakeState(self,state=None):

		"""
			Ability to Wake and Sleep Device
			if state variable is unused, you can detect the device state
			state variable can be "Awake" or "Asleep"
		"""


		shell_response = self.device.shell('dumpsys power | grep mWakefulness')

		if state == 'Awake':
			if 'Asleep' in shell_response:
				self.device.input_keyevent(26)
			return True
		elif state == 'Asleep':
			if 'Awake' in shell_response:
				self.device.input_keyevent(26)
			return True


		if 'Awake' in shell_response:
			return 'Awake'
		elif 'Asleep' in shell_response:
			return 'Asleep'
		else:
			return 'Unable To Determine'


	########################
	# CHECK KEYBOARD STATE #####################
	########################

	def CheckKeyboardOnscreen(self,hide=False):

		"""
			Returns True if keyboard is displayed on screen and False if otherwise
		"""

		shell_response = self.device.shell('dumpsys window InputMethod | grep "mHasSurface"')

		if hide is True:
			if 'mHasSurface=true' in shell_response:
				self.device.input_keyevent(111)
			return False

		if 'mHasSurface=true' in shell_response:
			return True

		else:
			return False


	################################
	# GET ALL TEXT VIA RESOURCE ID #####################
	################################

	def GetAllText(self,id,data=None,include_bounds=False):

		"""
			Get all texts via resource id
		"""

		if data is None:
			data = self.GetData()

		soup = BeautifulSoup(data,"html.parser").find_all(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{id}$',re.I)})

		results = []

		if include_bounds is True:
			for i in soup:
				results.append( (i['text'],i['bounds'].strip('[').strip(']').replace('][',',').split(',')))
		else:
			for i in soup:
				results.append(i['text'])
		
		return results


	########################
	# CLICK BOUND DIRECTLY #####################
	########################

	def ClickBound(self,bounds,margin=0): # New Click Direct Version
		minx, miny, maxx, maxy = bounds
		self.device.input_tap(randint(int(minx) + margin, int(maxx) - margin), randint(int(miny) + margin, int(maxy) - margin))


	#########################
	# GET DEVICE RESOLUTION #####################
	#########################

	def GetScreenResolution(self):
		results = [int(i) for i in self.device.shell('wm size').strip('Physical size: ').strip('\n').split('x')]

		return results








	
if __name__ == "__main__":

	instagram = Device('MNV9K19314903315')
	results = instagram.GetScreenResolution()
	
	print(results)



	