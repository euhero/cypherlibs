from sqlalchemy import create_engine, String, Integer, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Base = declarative_base()

class MyDb:
	def __init__(self,db,db_location,Base):

		self.engine = create_engine(f'sqlite:///{db_location}')

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
			if self.Query().filter_by(**data).first() is not None:
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
			return False

	def Query(self):
		result = self.session.query(self.db)
		return result





if __name__ == "__main__":
	pass
	# class Notification_Db(Base):
	# 	__tablename__ = 'notifications'

	# 	rowid = Column('rowid',Integer,primary_key=True)
	# 	deviceid = Column('deviceid',String)
	# 	account = Column('account',String) 
	# 	notification = Column('notification',String) 
	# 	date = Column('date',String,default=str(datetime.datetime.now().date()) )
	# 	time = Column('time',String,default=str(datetime.datetime.now().time())) 




	# NotificationDb = MyDb(Notification_Db,'notificationdatabase.db')
