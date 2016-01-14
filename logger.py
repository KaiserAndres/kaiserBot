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
		newId = open("logIds.dat", "w")
		newId.write(str(idNumber+1))
		newId.close()
	except:
		idNumber = 0
		newId = open("logIds.dat", "w")
		newId.write(str(idNumber+1))
		newId.close()

	return idNumber

