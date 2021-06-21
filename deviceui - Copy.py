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
import subprocess


class Device:
	def __init__(self,deviceid,app="instagram",wirelessip=None,Pt=None):

		subprocess.call('adb devices',shell=True,stdout=subprocess.PIPE)

		apps = {
			"instagram" : "com.instagram.android/com.instagram.android.activity.MainTabActivity",
			"tiktok" : "com.ss.android.ugc.trill/com.ss.android.ugc.aweme.splash.SplashActivity",
			"linkedin" : "com.linkedin.android.salesnavigator/com.linkedin.android.salesnavigator.ui.home.HomeV2Activity",
			"twitter" : "com.twitter.android/com.twitter.android.StartActivity"
		}

		try:
			self.app = apps[app]
		except KeyError:
			self.app = app
		self.mainapp_name = self.app.split('/')[0]

		client = AdbClient(host="127.0.0.1", port=5037)
		self.device = client.device(deviceid)
		self.deviceid = deviceid

		# self.GetData = self.MainGetData

		if not os.path.isdir(deviceid):
			os.mkdir(deviceid)

		self.Pt = Pt
		self.GetDataFilter = None

		if deviceid not in subprocess.getoutput('adb devices'):
			self.Printhis(f'Device ID is not plugged in : {deviceid}','red')
			sys.exit(0)

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
			if idleerror % 5 == 0 and idleerror != 0:
				self.SwipeScreen("scrollup",message='Trying to prevent idle error')
			if idleerror == 30:
				self.Printhis(message="Please Try Restarting your device before continuing",color="red")
				return False
			devicexml = self.device.shell("uiautomator dump", timeout=60)
			if check_dumpdata_try == 30:
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

	def GetData(self,check=True,charlimit=8000,GetdataFilter=True, source=None):

		if source is None:
			source = self.deviceid + '/data.xml'

		
		if check is False:
			if self.DumpData() is False:
				self.Printhis(message="Data Returning False from getdata | with check false",color='log')
				self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color='yellow')
				sys.exit(0)
			self.device.pull('/sdcard/window_dump.xml', self.deviceid + '/data.xml')
			with open(source, 'r', encoding="UTF-8") as data:
				data = data.read().encode(encoding="UTF-8")
			

			if GetdataFilter is True:
				if callable(self.GetDataFilter):
					self.GetDataFilter(data)

			return data

		data = 'None'
		error = 0
		while len(data) < charlimit:
			if self.DumpData() is False:
				self.Printhis(message="Data Returning False from getdata | with check true",color="log")
				self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color="yellow")
				sys.exit(0)
			self.device.pull('/sdcard/window_dump.xml', self.deviceid + '/data.xml')
			with open(source, 'r', encoding="UTF-8") as data:
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


			if GetdataFilter is True:
				if callable(self.GetDataFilter):
					self.GetDataFilter(data)

		return data


	############################################
	# BEGINING OF CONTROLS                     #################################################################################################################################
	############################################

	###############
	# RESOURCE ID #####################
	###############

	def Resourceid(self,id, hold=False, sec=5000, check=False, checkandclick=False, sleep=0.5, data='None',margin=(0,0,0,0)):

		if isinstance(margin,int):
			margin = [margin for _ in range(4)]

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

	def Textid(self,id, hold=False, sec=5000, check=False, checkandclick=False, resourceid='None', sleep=0.5, data='None',margin=(0,0,0,0), get_coordinate=False):

		if isinstance(margin,int):
			margin = [margin for _ in range(4)]
		
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

		if get_coordinate is True:
			return x

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

		if isinstance(margin,int):
			margin = [margin for _ in range(4)]

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

	##############
	# CLASS ID #####################
	##############

	def Classid(self,id, hold=False, sec=5000, check=False, checkandclick=False, resourceid='None', sleep=0.5, data='None', margin=(0,0,0,0)):

		if isinstance(margin,int):
			margin = [margin for _ in range(4)]

		resourceid = resourceid
		if data == 'None':
			data = self.GetData()
			time.sleep(sleep)
		if resourceid != 'None':
			x = BeautifulSoup(data,"html.parser").find(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{resourceid}$',re.I),"class":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
			minx, miny, maxx, maxy = x

			minx = int(minx) + margin[0]
			miny = int(miny) + margin[1]
			maxx = int(maxx) - margin[2]
			maxy = int(maxy) - margin[3]

			self.device.input_tap(randint(int(minx), int(maxx)), randint(int(miny), int(maxy)))
			return True

		if check == True:
			try:
				x = BeautifulSoup(data,'html.parser').find(attrs={"class":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
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

		x = BeautifulSoup(data,'html.parser').find(attrs={"class":re.compile(f'^{id}$',re.I)})['bounds'].strip('[').strip(']').replace('][',',').split(',')
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


	def OpenApp(self,apptoopen=None):
		if apptoopen is None:
			self.device.shell(f"am start -n {self.app}")
		else:
			self.device.shell(f"am start -n {apptoopen}")

	###############
	# CLOSE APP #####################
	###############		

	def CloseApp(self):
		self.device.shell(f"am force-stop {self.mainapp_name}")

	#################
	# OPEN VIA LINK #####################
	#################

	def OpenLink(self,link,openapp=None):
		if openapp is None:
			openapp = self.mainapp_name
		self.device.shell(f'am start -a "android.intent.action.VIEW" -d "{link}" {openapp}')

	###########################
	# WRITING TEXT WITH SPACE #####################
	###########################

	def WriteText(self,text):
		text = text.replace('’',"'")
		text = text.replace('‘',"'")
		text = text.replace('\r\n','\n')
		text = text.replace("\\n","\n")
		text = text.replace("\\","\\\\")
		text = text.replace("$","\$")
		text = text.split(" ")

		word_storage = []
		for n,word in enumerate(text,start=1):
			# self.device.input_text(word)
			# if n != len(text):
			# 	self.device.input_text("%s")

			word_storage.append(word)

			if len(word_storage) >= 5:
				self.device.input_text("%s".join(word_storage))
				if n != len(text):
					self.device.input_text("%s")
				word_storage = []
			
		if len(word_storage) > 0:
			self.device.input_text("%s".join(word_storage))


	####################
	# PAGE LOAD CHECKS #####################
	####################

	def PageLoadCheck(self,mustexist,ui="text",shouldcontinue=False,retry=15,data=None,message='Waiting for page to load'):
		""" mustexist takes lists """
		pagecheckererror = 0
		finish_message = lambda x : self.Printhis(f'{x}', 'vanishgreen')
		if data is None:
			data = self.GetData(check=False)
		
		loading_animation = lambda x : 4 if x % 4 == 0 else 3 if x % 3 == 0 else 2 if x % 2 == 0 else 1
		while True:
			self.Printhis(f"{message}" + '.' * loading_animation(pagecheckererror + 1),'vanish')

			for words in mustexist:
				if ui == "text":
					if self.Textid(words,check=True,data=data) is True:
						finish_message(message)
						return True
				if ui == "resource-id":
					if self.Resourceid(words,check=True,data=data) is True:
						finish_message(message)
						return True
				if ui == "content-desc":
					if self.Contentid(words,check=True,data=data) is True:
						finish_message(message)
						return True
			if pagecheckererror == retry:
				if shouldcontinue is False:
					self.Printhis(message='Page did not load correctly. Restarting Bot...'.ljust(20),color="vanish")
					self.Printhis(message="##### Bot is ReStarting Using Excemption #####",color="yellow")
					self.Printhis(message='Exception Raised Because PageLoadCheck Failed',color='log')
					sys.exit(0)
				if shouldcontinue is True:
					return False
			data = self.GetData(check=False)
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

	def SwipeScreen(self,method,times=1,message="Scrolling feed",delay=None):

		""" method :
				scrolldown
				scrollup
			times :
				default 1 """

		if method == "scrolldown":
			for i in range(times):
				self.Printhis(message=message + '.' * i,color="vanish")
				self.device.input_swipe(randint(197, 428), randint(748, 763), randint(197, 428), randint(548, 563), 500)
				if delay is not None:
					for i in range(int(delay)):
						self.Printhis(f"Sleeping {i+1}/{delay}","vanish")
						time.sleep(1)
		elif method == "scrollup":
			for i in range(times):
				self.Printhis(message=message + '.' * i,color="vanish")
				self.device.input_swipe(randint(197, 428), randint(548, 563), randint(197, 428), randint(748, 763), 500)
				if delay is not None:
					for i in range(int(delay)):
						self.Printhis(f"Sleeping {i+1}/{delay}","vanish")
						time.sleep(1)
		else:
			start_x, start_y, end_x, end_y = method
			for i in range(times):
				self.device.input_swipe(start_x, start_y, end_x, end_y, 500)
				if delay is not None:
					for i in range(int(delay)):
						self.Printhis(f"Sleeping {i+1}/{delay}","vanish")
						time.sleep(1)

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
		
		result = self.device.shell("dumpsys window windows")
		result = re.findall('com.instagram.*/',result)[0]
		result = result.replace('/','')

		return result

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

	def GetAllText(self,id,ui='resource-id',data=None,include_bounds=False,bounds_only=False,source_only=False):

		"""
			Get all texts via resource id
		"""

		if data is None:
			data = self.GetData()

		if ui == 'resource-id':
			soup = BeautifulSoup(data,"html.parser").find_all(attrs={"resource-id":re.compile(f'^{self.mainapp_name}:id/{id}$',re.I)})
		elif ui == 'text':
			soup = BeautifulSoup(data,"html.parser").find_all(attrs={"text":re.compile(f'^{id}$',re.I)})

		if source_only is True:
			return soup

		results = []

		if bounds_only is True:
			for i in soup:
				results.append( i['bounds'].strip('[').strip(']').replace('][',',').split(','))
			return results

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

	####################
	# UI COMMON ACTION #####################
	####################

	def KeyEvent(self,action):
		"""
			Key Event for controlling phones
		
			Available action : 
			back
			home
			menu
			enter

		"""

		if action == 'back':
			self.device.input_keyevent('4')
		elif action == 'hone':
			self.device.input_keyevent('3')
		elif action == 'menu':
			self.device.input_keyevent('82')
		elif action == 'enter':
			self.device.input_keyevent('66')

	####################
	# DELETE APP DATA #####################
	####################

	def DeleteAppData(self):
		self.device.shell(f"pm clear {self.mainapp_name}")
		return True


if __name__ == "__main__":
	pass


	# def GetData(**kwargs):

	# 	data = ig.MainGetData(**kwargs)

	# 	if "Action Blocked" in str(data):
	# 		# ig.Print("Looks Like Action is Blocked", color="red")
	# 		try:
	# 			ig.Textid('Tell us', data=data)
	# 		except:
	# 			ig.Textid('OK',data=data)

	# 	if ig.Textid("Try Again Later",check=True, data=data) is True:
	# 		ig.Textid('Tell us',check=True,checkandclick=True, data=data)
	# 		ig.Textid('OK',check=True,checkandclick=True,data=data)

	# 	# if ig.Textid(f"You've been logged out of {current_account['account']}. The account owner may have changed the password.",check=True, data=data) is True:
	# 	# 	ig.Snapshot(filename=f'Logged Out {current_account["account"]}')
			
	# 		# notificationdb.Add(deviceid=deviceid,account=current_account["account"],notification='Youve been Logged Out')
	# 		# with open('notification.txt','a') as notification:
	# 		# 	notification.writelines(f'{current_account["account"]}-{deviceid},Youve been Logged Out ({datetime.datetime.now().date()})\n')				
	# 		ig.Textid('OK',check=True,checkandclick=True,data=data)
	# 		sys.exit(0)

	# 	return data

	ig = Device('MNV9K19314903315')
	ig.GetData()
	# print(ig.GetCurrentFocus())

