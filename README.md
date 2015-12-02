
            _    ____ ___   __     ___       _ _             _
           / \  / ___|_ _|  \ \   / (_) __ _(_) | __ _ _ __ | |_ ___
          / _ \| |    | |____\ \ / /| |/ _` | | |/ _` | '_ \| __/ _ \
         / ___ \ |___ | |_____\ V / | | (_| | | | (_| | | | | ||  __/
        /_/   \_\____|___|     \_/  |_|\__, |_|_|\__,_|_| |_|\__\___|
                                       |___/
    
                  == Configuration Change Monitoring Tool ==


Introduction
=============
ACI Vigilante is a simple tool to monitor the status of a fabric and detect 
changes to any of the existing tenants. It can currently monitor all existing
and new tenants created on the fabric and any of their child objects. 

Requirements
=============
- Python 2.7 or Python3.3 or above.
- The "acitoolkit" library
  - Download it from the following URL and install it using "python2.7 setup.py install"
    - https://github.com/datacenter/acitoolkit

Usage
=====

    $ aci-vigilante.py 

The application also takes the regular parameters for APIC address, username and 
password, as well as parses any existing *credentials.py* file stored in the
same directory. In that case, the content of the *credentials.py* file must 
follow this format:

    URL="https://192.168.0.90"
    LOGIN="admin"
    PASSWORD="Ap1cPass123"

If the *credentials.py* does not exist and the credentials are not supplied from
the command line, the application will ask for them interactively.

Usage Examples
==============

    $ python3 aci-vigilante.py
    $ python3 aci-vigilante.py --debug yes
    $ python3 aci-vigilante.py -l admin -p "Ap1cPass123" -u "https://192.168.0.90"


Output Examples
===============

    $ python3 aci-vigilante.py
            _    ____ ___   __     ___       _ _             _
           / \  / ___|_ _|  \ \   / (_) __ _(_) | __ _ _ __ | |_ ___
          / _ \| |    | |____\ \ / /| |/ _` | | |/ _` | '_ \| __/ _ \
         / ___ \ |___ | |_____\ V / | | (_| | | | (_| | | | | ||  __/
        /_/   \_\____|___|     \_/  |_|\__, |_|_|\__,_|_| |_|\__\___|
                                       |___/
               == Configuration Change Monitoring Tool ==
    [+] Successfully connected to https://10.48.59.234
    [+] Waiting for events...
    [+] fvTenant:uni/tn-Production was created
    [+] fvAp:uni/tn-Production/ap-E-Commerce-Platform was created
    [+] fvRtBd:uni/tn-common/BD-default/rtbd-[uni/tn-Production/ap-E-Commerce-Platform/epg-Web-Tier] was created
    [+] fvAEPg:uni/tn-Production/ap-E-Commerce-Platform/epg-Web-Tier was created
    [+] fvSubnet:uni/tn-Production/BD-App-Tier-BD/subnet-[10.0.10.254/24] was created
    [+] fvBD:uni/tn-Production/BD-App-Tier-BD was modified
    [+] fvSubnet:uni/tn-Production/BD-App-Tier-BD/subnet-[10.0.10.254/24] was modified
