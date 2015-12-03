# rhsmShowConsumerSubs
Script to Display Subscriptions consumed on Red Hat Subscription Management (RHSM)

# Overview

When working with Red Hat Subscription Management (RHSM), I have found the need
to easily identify which systems are consuming which subscriptions. This script assists
with that.

# Requirements

* Python (2.6 is what I've tested with)
* A valid username / password on the Red Hat Customer Portal

# Usage

~~~
$./rhsmShowConsumerSubs.py -l rh_user_account
~~~

# Notes

* The script will prompt for password if not provided
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
~~~
