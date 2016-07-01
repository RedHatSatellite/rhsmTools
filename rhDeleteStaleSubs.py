#!/usr/bin/env python

# File: rhDeleteStaleSubs.py
# Author: Zaina Afoulki <zaina@redhat.com>
# Purpose: Given a username, password and date, delete subscription
#                   for systems that didn't check in with RHSM  
#                   since the provided date.
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
import ssl
from optparse import OptionParser
from dateutil.parser import parse as parse_date
from datetime import datetime

parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user for RHSM", metavar="LOGIN")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD")
parser.add_option("-d", "--debug", dest='debug',help="print more details for debugging" , default=False, action='store_true')
parser.add_option("-c", "--last-checkin", dest="checkin", help="Last Check in Date in the format yyyy-mm-dd", metavar="CHECKIN")
(options, args) = parser.parse_args()

if not ( options.login ):
	print "Must specify a login (will prompt for password if omitted).  See usage:"
	parser.print_help()
	print "\nExample usage: ./rhDeleteStaleSubs.py -l rh_user_account -c 2016-02-10"
	sys.exit(1)
else:
    login = options.login
    password = options.password
    checkin = options.checkin

yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])

try:
    dt_reference = datetime.strptime(checkin, '%Y-%m-%d')
except ValueError:
    print "Incorrect format"

if not password: password = getpass.getpass("%s's password:" % login)

if hasattr(ssl, '_create_unverified_context'):
	        ssl._create_default_https_context = ssl._create_unverified_context

portal_host = "subscription.rhn.redhat.com"

url = "https://" + portal_host + "/subscription/users/" + login + "/owners/"
try:
 	request = urllib2.Request(url)
        if options.debug :
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
if options.debug :
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
#### verify the LastCheckin date associated with them. 
for consumer in consumerdata:
	consumerType = consumer["type"]["label"]
	lastCheckin = consumer["lastCheckin"]
	factsurl = "https://" + portal_host + "/subscription" + consumer["href"] + "/"
        if options.debug :
            print "Attempting to connect: " + factsurl
	try:
		sysinfo = urllib2.Request(factsurl)
		base64string = base64.encodestring('%s:%s' % (login, password)).strip()
		sysinfo.add_header("Authorization", "Basic %s" % base64string)
		sysresult = urllib2.urlopen(sysinfo)
		sysdata = json.load(sysresult)
	except Exception, e:
		print "FATAL Error - %s" % (e)
		sys.exit(1)
	if sysdata['facts'].has_key('network.ipv4_address'):
		ipaddr = sysdata['facts']['network.ipv4_address']
	else:
		ipaddr = "Unknown"

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
		dt = parse_date(lastCheckin)
		dt_no_tzinfo = dt.replace(tzinfo=None)
		if dt_no_tzinfo <= dt_reference:
			print "%s IP %s last checked-in %s which is older than %s. Delete? y/n" % (consumer["name"],ipaddr,dt_no_tzinfo,dt_reference)
			choice = raw_input().lower()
			if choice in yes:
				# Delete System's Subscription from RHSM
				print "Removing System's Subscription from RHSM..."
			elif choice in no:
				# Skip this System
				pass
			else:
			   sys.stdout.write("Please respond with 'yes' or 'no'")
sys.exit(0)
