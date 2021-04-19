import os

class FileDataManager():
	def __init__(self,location):

		self.location = location

		if not os.path.isfile(f'{location}'):
			with open(f'{location}','w') as _:
				pass
	
	def write(self,data):
		with open(f'{self.location}','w' ,encoding="utf-8") as filedata:
			filedata.write(str(data))
		return True
	
	def read(self):
		with open(f'{self.location}','r') as filedata:
			return [i.strip('\n') for i in filedata.readlines()]

	def append(self,data,unique=False):
		if unique is True:
			if data in self.read():
				return True
		with open(f'{self.location}','a', encoding="utf-8") as filedata:
			filedata.writelines(str(data)+'\n')
		return True

	def delete_line(self,data):
		current_records = self.read()

		current_records.remove(data)
		self.write('')
		[self.append(record) for record in current_records]

		return True
