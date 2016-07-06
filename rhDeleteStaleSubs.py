#!/usr/bin/env python

# File: rhDeleteStaleSubs.py
# Author: Zaina Afoulki <zaina@redhat.com>
# Purpose: Given a username, password and date, delete subscriptions
#                   for systems that didn't check in with RHSM since
#                   the provided date.
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
import httplib
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
parser.add_option("-c", "--last-checkin", dest="checkin", help="Last Date a System checked in with RHSM, format yyyy-mm-dd", metavar="CHECK-IN")
parser.add_option("-f", "--force", dest="force", help="Do not ask prompt for confirmation, unregister all systems that match the last-checkin criteria", default=False, action='store_true')
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
    force = options.force

try:
    dt_reference = datetime.strptime(checkin, '%Y-%m-%d')
except ValueError:
    print "Incorrect Date format. Please use %Y-%m-%d. Example usage: ./rhDeleteStaleSubs.py -l rh_user_account -c 2016-02-10"
    sys.exit(1)

if not password: password = getpass.getpass("%s's password:" % login)

if hasattr(ssl, '_create_unverified_context'):
	        ssl._create_default_https_context = ssl._create_unverified_context

portal_host = "subscription.rhn.redhat.com"

url = "https://" + portal_host + "/subscription/users/" + login + "/owners/"
try:
 	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except Exception, e:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

accountdata = json.load(result)
for accounts in accountdata:
	acct = accounts["key"]

#### Grab a list of Consumers
url = "https://" + portal_host + "/subscription/owners/" + acct + "/consumers/"
try:
 	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except Exception, e:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

consumerdata = json.load(result)

#### Now that we have a list of Consumers, loop through them and 
#### verify the LastCheckin date associated with them. 
for consumer in consumerdata:
	consumerType = consumer["type"]["label"]
	lastCheckin = consumer["lastCheckin"]
	factsurl = "https://" + portal_host + "/subscription" + consumer["href"] + "/"
	if lastCheckin is not None:
		dt = parse_date(lastCheckin)
		dt_no_tzinfo = dt.replace(tzinfo=None)
		if dt_no_tzinfo <= dt_reference:
			print "Hostname: %s UUID:%s last checked-in %s which is older than %s" % (consumer["name"],
				consumer["uuid"], dt_no_tzinfo.strftime("%Y-%m-%d"), 
				dt_reference.strftime("%Y-%m-%d"))
			choice = None
			if not options.force: 
				choice = raw_input("Unregister? y/n ").lower()
			if choice in ['yes','y'] or options.force:
				print "Removing System's Subscription from RHSM..."
				try:
					request = urllib2.Request(factsurl)
					base64string = base64.encodestring('%s:%s' % (login, password)).strip()
					request.add_header("Authorization", "Basic %s" % base64string)
					request.get_method = lambda: 'DELETE'
					result = urllib2.urlopen(request)
				except Exception, e:
					print "FATAL Error - %s" % (e)
sys.exit(0)
