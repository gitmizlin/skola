#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example to show how command-line options can be handled by a script.
"""

import sys
import os
from datetime import datetime
import getopt
import pdb
import requests

#
# Add some stuff about this script
#
PROGRAM = os.path.basename(sys.argv[0])
AUTHOR = "Mi"
EMAIL = "miis15@student.bth.se"
VERSION = "1.0"
USAGE = """{program} - AUTHOER: {author} ({email}), version {version}

Usage:
  {program} [options] name

Options:
    -h, --help skall visa en hjälptext som beskriver ditt kommando och hur det används.
    -v, --version skall visa versionen av programmet.
    --verbose skall innebära att mer text skrivs ut, kanske bra för debugging?
    -s, --silent skall innebära att minimalt med utskrift sker, bra om man bara vill se svaret.
    -p, --ping skall hämna en webbsida.

  name                           Your name.
""".format(program=PROGRAM, author=AUTHOR, email=EMAIL, version=VERSION)

MSG_VERSION = "{program} version {version}.".format(program=PROGRAM, version=VERSION)
MSG_USAGE = "Use {program} --help to get usage.\n".format(program=PROGRAM)

#
# Global default settings affecting behaviour of script in several places
#
SILENT = False
VERBOSE = True
NAME = ""

EXIT_SUCCESS = 0
EXIT_USAGE = 1
EXIT_FAILED = 2

def printUsage(exitStatus):
    """
    Print usage information about the script and exit.
    """
    print(USAGE)
    sys.exit(exitStatus)

def printVersion():
    """
    Print version information and exit.
    """
    print(MSG_VERSION)
    sys.exit(EXIT_SUCCESS)

def pingWebsite():
    """
    Ping a website.
    """
    url = "http://google.com"
    req = requests.head(url)

    print("Request to ", url)
    print("Recieved status code: ", req.status_code)

def parseOptions():
    """
    Merge default options with incoming options and arguments and return them as a dictionary.
    """

    # Switch through all options
    try:
        global VERBOSE

        opts, args = getopt.getopt(sys.argv[1:], "d:hr:sv", ["ping", "help", "version", "silent", "verbose"])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printUsage(EXIT_SUCCESS)

            elif opt in ("-p", "--ping"):
                pingWebsite()

            elif opt in ("-v", "--version"):
                printVersion()

            elif opt in ("--verbose"):
                VERBOSE = True

            elif opt in ("-s", "--silent"):
                VERBOSE = False

            else:
                assert False, "Unhandled option"

        if len(args) != 1:
            assert False, "Missing name"

        print(args)

        # The name passed as a required argument
        global NAME
        NAME = args[0]

    except Exception as err:
        print(err)
        print(MSG_USAGE)
        # Prints the callstack, good for debugging, comment out for production
        #traceback.print_exception(Exception, err, None)
        sys.exit(EXIT_USAGE)


def main():
    """
    Main function to carry out the work.
    """
    startTime = datetime.now()

    parseOptions()

    timediff = datetime.now()-startTime
    if VERBOSE:
        sys.stderr.write("Script executed in {}.{} seconds\n".format(timediff.seconds, timediff.microseconds))

    sys.exit(EXIT_SUCCESS)



if __name__ == "__main__":
    main()
