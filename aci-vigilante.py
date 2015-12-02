#!/bin/python
################################################################################
#            _    ____ ___   __     ___       _ _             _                #
#           / \  / ___|_ _|  \ \   / (_) __ _(_) | __ _ _ __ | |_ ___          #
#          / _ \| |    | |____\ \ / /| |/ _` | | |/ _` | '_ \| __/ _ \         #
#         / ___ \ |___ | |_____\ V / | | (_| | | | (_| | | | | ||  __/         #
#        /_/   \_\____|___|     \_/  |_|\__, |_|_|\__,_|_| |_|\__\___|         #
#                                       |___/                                  #
#                                                                              #
#                  == Configuration Change Monitoring Tool ==                  #
#                                                                              #
################################################################################
#                                                                              #
# [+] Written by:                                                              #
#  |_ Luis Martin (lumarti2@cisco.com)                                         #
#  |_ CITT Software CoE.                                                       #
#  |_ Cisco Advanced Services, EMEAR.                                          #
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2015-2016 Cisco Systems                                        #
# All Rights Reserved.                                                         #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, this software  #
#    is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF   #
#    ANY KIND, either express or implied.                                      #
#                                                                              #
################################################################################

# Standard Imports
import sys
import json
import time

# External library imports:
from acitoolkit.acitoolkit import Session, Credentials, Tenant
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Internal imports
from tools import *

# List of classes we are not interested in.
not_interesting_classes = ['fvReportingNode']

# FUNCTIONS
def print_banner():
    output("        _    ____ ___   __     ___       _ _             _        ", start="")
    output("       / \  / ___|_ _|  \ \   / (_) __ _(_) | __ _ _ __ | |_ ___  ", start="")
    output("      / _ \| |    | |____\ \ / /| |/ _` | | |/ _` | '_ \| __/ _ \ ", start="")
    output("     / ___ \ |___ | |_____\ V / | | (_| | | | (_| | | | | ||  __/ ", start="")
    output("    /_/   \_\____|___|     \_/  |_|\__, |_|_|\__,_|_| |_|\__\___| ", start="")
    output("                                   |___/                          ", start="")
    output("           == Configuration Change Monitoring Tool ==             ", start="")


def do_something(event_data):
    """
    This function is called everytime the state of an object changes, with
    a copy of the object itself. Note that this only applies to objects within
    a tenant, not fabric or other types of objects.
    
    This function can be customized to your needs to do fancy stuff everytime
    a change is detected.
    """
    for obj in event_data['imdata']:
        for key in obj:
            if "Rs" not in key and key not in not_interesting_classes:
                output("%s:%s was %s" % (key, obj[key]['attributes']['dn'], obj[key]['attributes']['status'])  )


# Start of the execution
if __name__ == "__main__":

    # Argument parsing. We use the ACI toolkit logic here, which tries to
    # retrieve credentials from the following places:
    # 1. Command line options
    # 2. Configuration file called credentials.py
    # 3. Environment variables
    # 4. Interactively querying the user
    # At the end, we should have an object args with all the necessary info.
    description = 'APIC credentials'
    creds = Credentials('apic', description)
    creds.add_argument('-d', "--debug", default=None, help='Enable Debug mode')
    args = creds.get()
    
    # Process all relevant command-line parameters and print our welcome banner
    if args.debug is not None:
        debug_enable()
    print_banner()
    
    # Now, we log into the APIC
    session = Session(args.url, args.login, args.password)
    response = session.login()
    if response.ok is False:
        fatal(response.content)
    else:
        output("Successfully connected to %s" % args.url)

    # Retrieve the list of existing tenants
    tenants = Tenant.get(session)
    
    # Subscribe to each one
    urls=[]
    for tn in tenants:
        url = "/api/mo/uni/tn-%s.json?query-target=subtree&subscription=yes" % tn.name
        try:
            debug("Subscribing to '%s'" % url)
            session.subscribe(url, only_new=True)
            urls.append(url)
        except:
            error("Error creating subscription for tenant '%s'" % tn.name)

    # Also, subscribe to the Tenant class so we can create new subscriptions
    # if new tenants get created.
    tn_url = "/api/class/fvTenant.json?subscription=yes"
    session.subscribe(tn_url, only_new=True)

    # Now we loop forever, waiting for any events
    output("Waiting for events...")
    while(True):
        
        # Check status of existing tenants
        for url in urls:
            if session.has_events(url):
                event_data = session.get_event(url)
                do_something(event_data)
        
        # Check for new tenants (if any tenants get added, we create a new
        # subscription; if they get deleted, we remove the existing one).
        if session.has_events(tn_url):
            tn = session.get_event(tn_url)
            tn_dn = tn['imdata'][0]['fvTenant']['attributes']['dn']
            url = "/api/mo/%s.json?query-target=subtree&subscription=yes" % tn_dn
            if tn['imdata'][0]['fvTenant']['attributes']['status']=="created":
                debug("Subscribing to '%s'" % url)
                session.subscribe(url, only_new=True)
                urls.append(url)
            elif tn['imdata'][0]['fvTenant']['attributes']['status']=="deleted":
                debug("Unsubscribing from '%s'" % url)
                session.unsubscribe(url)
                urls.remove(url)
            do_something(tn)

        # That was exhausting! Rest for a bit so we don't clog the CPU with 
        # a busy loop.
        time.sleep(0.1)

    sys.exit(0)
