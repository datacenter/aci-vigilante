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

# Standard library imports
import sys

# Globals
g_do_debug=False

# FUNCTION DEFINITIONS
def fatal(msg, start="[F] FATAL: "):
    """
    Prints and error message and aborts program execution
    """
    sys.stderr.write(start + str(msg) + "\n")
    sys.exit(1)

def warning(msg, start="[W] WARNING: "):
    """
    Prints a warning message to stderr
    """
    sys.stderr.write(start + str(msg) + "\n")
    
def error(msg, start="[E] ERROR: "):
    """
    Prints a warning message to stderr
    """
    sys.stderr.write(start + str(msg) + "\n")
    
def output(msg, start="[+] "):
    """
    Prints a message to stdout
    """
    sys.stdout.write(start + str(msg) + "\n")

def debug(msg, start="[D] "):
    """
    Prints a message to stdout only if the global g_do_debug var is True
    """
    global g_do_debug
    if g_do_debug==True:
        sys.stdout.write(start + msg+"\n")

def debug_enable():
    """
    Enables debug mode
    """
    global g_do_debug
    g_do_debug=True

