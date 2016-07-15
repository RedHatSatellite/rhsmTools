# rhsmShowConsumerSubs
Script to Display Subscriptions consumed on Red Hat Subscription Management (RHSM)

# rhDeleteStaleSubs.py
Script to Unregister systems that didn't check-in with RHSM since a given date.

# Overview

When working with Red Hat Subscription Management (RHSM), I have found the need
to easily identify which systems are consuming which subscriptions. The script 
rhsmShowConsumerSubs assists with that.

If you have systems that did not check-in with Red Hat Subscription Management 
(RHSM) for several days/weeks, it is likely that they are either powered off 
or deleted (in the case of a cloud/virtualized environment). 
rhDeleteStaleSubs.py will detect which systems haven't checked in since a 
given date YYYY-MM-DD and ask for confirmation to unregister them. There is
also a --force option to skip the confirmation and a --filter option to match 
a certain hostname pattern.

# Requirements

* Python (2.6 is what I've tested with)
* A valid username / password on the Red Hat Customer Portal

# Usage

~~~
$python rhsmShowConsumerSubs.py -l rh_user_account
$python rhDeleteStaleSubs.py -lrh_user-account --last-checkin 2016-06-05 
~~~

# Notes

* The scripts will prompt for password if not provided
* The **https_proxy** environmental variable, if set, will be used to connect via a proxy

### Example Output

~~~
$./rhsmShowConsumerSubs.py -l rh_user_account
Attempting to connect: https://subscription.rhn.redhat.com/subscription/users/rh_user_account/owners/
Attempting to connect: https://subscription.rhn.redhat.com/subscription/owners/1234567/consumers/
Name, Consumer Type, Contract Number, Product Name, Start Date, End Date, Quantity, Last Checkin, Username
My_Satellite_App,satellite,12345678,Red Hat Satellite Capsule Server,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,7,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,Red Hat Enterprise Linux Server, Premium (Physical or Virtual Nodes),2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,13,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,Red Hat Enterprise Linux Server, Standard (Physical or Virtual Nodes),2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,24,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,High Availability,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,10,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,87654321,Red Hat Cloud Infrastructure, Premium (2-sockets),2014-07-03T04:00:00.000+0000,2015-07-03T03:59:59.000+0000,3,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,High Availability,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,10,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,Red Hat Enterprise Linux Server, Premium (1-2 sockets) (Unlimited guests),2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,5,2015-08-02T10:42:24.000+0000,admin_user
My_Satellite_App,satellite,12345678,Red Hat Enterprise Linux for Virtual Datacenters, Premium,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,8,2015-08-02T10:42:24.000+0000,admin_user
satellite.example.net,system,12345678,Red Hat Enterprise Linux Server, Premium (1-2 sockets) (Unlimited guests),2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,3,2015-08-02T10:42:24.000+0000,admin_user
satellite.example.net,system,12345678,Red Hat Enterprise Linux Server, Standard (Physical or Virtual Nodes),2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,24,2015-08-02T10:42:24.000+0000,admin_user
satellite.example.org,system,12345678,Red Hat Satellite,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,10,2015-08-02T10:42:24.000+0000,admin_user
satellite.example.net,system,12345678,Red Hat Satellite,2014-10-08T04:00:00.000+0000,2015-10-08T03:59:59.000+0000,10,2015-08-02T10:42:24.000+0000,admin_user

$./rhDeleteStaleSubs.py -l rh_user_account --last-checkin 2016-07-04 --filter test
[DEBUG] Authentication successful
[DEBUG] Grabbing a list of systems
[DEBUG] Checking 28 subscribed systems...
Hostname: rhel6-test UUID:25483352-524a-4c24-9072-c484dc7829a9 last checked-in 2016-05-12 which is older than 2016-07-04
Unregister? y/n n
Hostname: rhel7-test UUID:a5675b75-746f-49ed-8631-c48a275f8495 last checked-in 2016-05-26 which is older than 2016-07-04
Unregister? y/n y
Removing System's Subscription from RHSM...
~~~
