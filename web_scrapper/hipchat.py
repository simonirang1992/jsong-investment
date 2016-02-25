#!/usr/bin/env python
import json
import requests
import sys

def err_hipchat(errmsg):
	errmsg = str(errmsg)
	try:
		msg="@Simon @JaySong ERROR OCCURRED"
		aurl='https://api.hipchat.com/v2/room/1864270/notification'
		headers = {'Authorization':'Bearer cK4Yz7wzBRMIAFdkHLC2yMhWMSKUldaxFpU9iRhI', 'Content-type':'application/json'}
		requests.post(url = aurl, data = json.dumps({'message':msg, 'color':'red','notify':True, 'message_format':'text'}), headers = headers)
		requests.post(url = aurl, data = json.dumps({'message':errmsg}), headers = headers)
	except requests.exceptions.RequestException as e:
		outerr = 'Fatal Error Encountered: %s' % e.strerror
		syslog.syslog(outerr)
