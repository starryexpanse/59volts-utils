#!/usr/bin/env python

# Very small example of the usage of DreamPyLib

import dreampylib


# Dreamhost test API account:
user = 'apitest@dreamhost.com'
key  = '6SHU5P2HLDAYECUM'

# Specify the default returntype.
# Can be either 'dict' or 'list', and is dict by default
defaultReturnType = 'dict'   

# Initialize the library and open a connection
connection = dreampylib.DreampyLib(user,key)
   
# If the connection is up, do some tests.
if connection.IsConnected():
	
	# For instance, list the available commands:
	print 'Available commands:\n ',
	listOfCommands = connection.AvailableCommands()
	print '\n  '.join(listOfCommands)
	
	print connection.dreamhost_ps.list_ps()
	
	# Even if defaultReturnType is 'dict', you can get the last result as a list, too.

	connection.dreamhost_ps.list_size_history(ps = 'ps7093')
	print connection.ResultList()
	
	# Let's also print the keys so we know what we're looking at
	print connection.ResultKeys()
	
	
	#print connection.mysql.list_dbs()
else:
	print "Error connecting!"
	print connection.Status()