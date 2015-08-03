#!/usr/bin/env python

# File: rhsmShowConsumerSubs.py
# Author: Rich Jerrido <rjerrido@outsidaz.org>
# Purpose: Given a username & password, query
# 		   Red Hat Subscription Management (RHSM) to show a
# 		   listing of consumers and their associated subscriptions
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import getpass
import urllib2
import base64
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user for SAM", metavar="LOGIN")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD")
(options, args) = parser.parse_args()

if not ( options.login ):
	print "Must specify a login (will prompt for password if omitted).  See usage:"
	parser.print_help()
	print "\nExample usage: ./rhsmShowConsumerSubs.py -l rh_user_account "
	sys.exit(1)
else:
	login = options.login
	password = options.password


if not password: password = getpass.getpass("%s's password:" % login)


portal_host = "subscription.rhn.redhat.com"

#### Grab the Candlepin account number
url = "https://" + portal_host + "/subscription/users/" + login + "/owners/"
try:
 	request = urllib2.Request(url)
	print "Attempting to connect: " + url
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

accountdata = json.load(result)
for accounts in accountdata:
	acct = accounts["key"]

#### Grab a list of Consumers
url = "https://" + portal_host + "/subscription/owners/" + acct + "/consumers/"
print "Attempting to connect: " + url

try:
 	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

consumerdata = json.load(result)

#### Now that we have a list of Consumers, loop through them and 
#### List the subscriptions associated with them. 
print "Name, Consumer Type, Contract Number, Product Name, Start Date, End Date, Quantity, Last Checkin"
for consumer in consumerdata:
	consumerType = consumer["type"]["label"]
	lastCheckin = consumer["lastCheckin"]
	detailedurl = "https://" + portal_host + "/subscription" + consumer["href"] + "/entitlements/"
	try:
		sysinfo = urllib2.Request(detailedurl)
		base64string = base64.encodestring('%s:%s' % (login, password)).strip()
		sysinfo.add_header("Authorization", "Basic %s" % base64string)
		sysresult = urllib2.urlopen(sysinfo)
		sysdata = json.load(sysresult)
	except Exception, e:
		print "FATAL Error - %s" % (e)
		sys.exit(1)
	for products in sysdata:
		productName = products["pool"]["productName"]
		contractNumber = products["pool"]["contractNumber"]
		startDate = products["startDate"]
		endDate = products["endDate"]
		quantity = products["pool"]["consumed"]
		print "%s,%s,%s,%s,%s,%s,%s,%s" % (consumer["name"],consumerType,contractNumber,productName,startDate,endDate,quantity,lastCheckin)


sys.exit(2)
