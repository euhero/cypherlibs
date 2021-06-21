import base64
from cryptography.fernet import Fernet


class CypherCrypt():
	def __init__(self):
		self.key = base64.urlsafe_b64encode(b'euheroeuheroeuheroeuheroeuheroeu')
		self.f = Fernet(self.key)
	def Cyencrypt(self,message):
		# Encrypt String
		# Enter String and it will automatically encode and decode to Encrypted String
		# Fernet only takes bytes only when encrypting
		return self.f.encrypt(message.encode()).decode()
	def Cydecrypt(self,encrypted):
		# Encrypt Encrypted String
		# Enter Encrypted String and it will automatically decode and encode to Decrypted String
		# Fernet only takes bytes only when decrypting
		return self.f.decrypt(encrypted.encode()).decode()

if __name__ == '__main__':
	def Cy():
		cy = CypherCrypt()
		choose = input('Type e to encrypt or Type d to decrypt : ')
		if choose == 'e':
			message = input('Enter String to Encrypt : ')
			print('----------------------------------------------------------------------------')
			print(cy.Cyencrypt(message))
			print('----------------------------------------------------------------------------')
		elif choose == 'd':
			try:
				message = input('Enter String to Decrypt : ')
				print('----------------------------------------------------------------------------')
				print(cy.Cydecrypt(message))
				print('----------------------------------------------------------------------------')
			except Exception as e:
				print('Invalid Encryption')
				print('----------------------------------------------------------------------------')
		else:
			Cy()
		Cy()
	Cy()