import datetime
from colorama import init, Fore, Back
import sys
import os

class Printhis:
	def __init__(self,folder_name='logs',logging=True):
		
		self.logging = logging
		self.folder_name = folder_name
		init(autoreset=True)

	def log(self,message,color='default',vanishlog=False):

		"""
			color :
			    default
			    green
			    red
			    yellow
			    log
			    vanish
			    vanishgreen
		"""

		message = f'{message}' + ' ' * 17

		if color == 'default':
			print(Fore.WHITE+ '[' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ']\t: ' + message)
		elif color == 'green':
			print(Fore.GREEN + '[' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ']\t: ' + message)
		elif color == 'red':
			print(Fore.RED + '[' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ']\t: ' + message)
		elif color == 'yellow':
			print(Fore.YELLOW + '[' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ']\t: ' + message)

		elif color == 'log':
			pass

		elif color == 'vanish':
			sys.stdout.write(f'\r[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: {message}\r')
			sys.stdout.flush()
			if vanishlog is False:
				return True

		elif color == 'vanishgreen':
			sys.stdout.write(f'\r{Fore.GREEN}[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: {message}\r')
			sys.stdout.flush()
			if vanishlog is False:
				return True

		if self.logging:

			if not os.path.isdir(self.folder_name):
				os.mkdir(self.folder_name)

			with open(self.folder_name + '/logs.txt', 'a', encoding="UTF-8") as logs:
				logs.writelines(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: {message}\n')

			if color == 'red':
				with open(self.folder_name + '/errorlogs.txt', 'a', encoding="UTF-8") as logs:
					logs.writelines(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]\t: {message}\n')