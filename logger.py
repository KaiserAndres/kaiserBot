'''
	Title: Logger man
    Author: Andrés Villagra de la Fuente
    Creation date: 00:05 14/01/2016 (GMT-3)
    Last edit: 00:05 14/01/2016 (GMT-3)
    Version: 1.0

    Description:
        This library will assist with the keeping of logs of irc conversations
    logs can be kept both as an HTML locument or a .txt file.
'''


def getFreeId():
	'''
		Returns a free id number as an integer.

		It reads from a logIds.dat file to get the last free id and updates it
	recording the new free id.
	'''
	try:
		newId = open("logIds.dat", "r")
		idNumber = int(newId.read())
		newId.close()
		updateFreeId(idNumber)
	except:
		#-----------------------------------------------------------------------
		#	Makes a new file in case one isn't found.
		#-----------------------------------------------------------------------
		idNumber = 0
		updateFreeId(idNumber)

	return idNumber


def updateFreeId(lastNumber, change = 1):
	'''
		Updates the value in the logIds file.

		lastNumber: Integer of the last used id
		change: Integer, describes how many numbers are skipped.
	'''
	newId = open("logIds.dat", "w")
	newId.write(str(lastNumber+change))
	newId.close()

class reader:

	'''
		logs the conversation and saves it to a file
	'''
	def __init__(self, room, logId = getFreeId()):
		'''	
			room: String with the following format:
				#<ROOM NAME>
				  This is the irc room that is listened for recording messages.
			logId: Integer with the last free id, unless specified will always
				   be the last available id.
		'''
		self.room = room
		self.logFile = open(str(logId)+".log", "w")

	def recordLine(self, user, message):
		'''
			Records the message from the user in the specific file

			user: string, name of the user.
			message: string, data sent by the user.
		'''
		try:
			if message[:2] != "((":
				self.logFile.write(user+": "+message+"\n")
		except:
			pass


