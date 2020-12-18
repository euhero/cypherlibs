from sqlalchemy import create_engine, String, Integer, ForeignKey, Column, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import random

# Base = declarative_base()

class MyDb:
	def __init__(self,db,db_location,Base):

		self.engine = create_engine(f'sqlite:///{db_location}',connect_args={'timeout': 15})

		# Create database if it doesn't exist
		Base.metadata.create_all(bind=self.engine)

		Session = sessionmaker(bind=self.engine)

		self.session = Session()
		self.db = db
		self.session.close()

	def SaveSession(self):
		self.session.commit()
		self.session.close()
		return True

	def Add(self,unique=False,**data):
		
		if unique is True:
			if self.query('first',**data) is not None:
				self.SaveSession()
				return False
		self.session.add(self.db(**data))
		if self.SaveSession() is True:
			return True

	def Delete(self,**data):
		try:
			self.session.delete(self.Query().filter_by(**data).first())
			if self.SaveSession() is True:
				return True
		except:
			self.SaveSession()
			return False

	def Query(self):
		result = self.session.query(self.db)
		return result

	def query(self,get,**filter_by):

		results = self.Query().filter_by(**filter_by)

		if get == 'first':
			results =  results.first()

			if results == None:
				results = None
			else:
				results = vars(results)


		elif get == 'all':
			results =  results.all()

			try:
				results = [vars(i) for i in results]
			except UnboundLocalError:
				results = None

		elif isinstance(get,int):
			results = results.order_by(func.random()).limit(get).all()

			try:
				results = [vars(i) for i in results]
				# if get > len(results):
				# 	get = len(results)
				# results = random.sample(results,get)
			except UnboundLocalError:
				results = None
		
		self.SaveSession()
		
		return results

	def Update(self,query,update):
		qresult = self.Query().filter_by(**query).first()
		for keys in update.keys():
			setattr(qresult,keys,update[keys])
		self.SaveSession()
		
		return True




if __name__ == "__main__":

	# deviceid = 'MNV9K19314903315'
	# account = 'gram.genius'

	



	pass
