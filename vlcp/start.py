#env python
'''
Created on 2015/10/19

:author: hubo

Command-line entry 
'''

from __future__ import print_function
from vlcp.server import main

import sys
import os.path
# No argparse
import getopt
doc = '''Run VLCP server from command line
[python|pypy] vlcp.py [-f <configfile>] [-d] [-p <pidfile>] [startmodule] ...
[python|pypy] vlcp.py --help

Available options:
  -f            Configuration file position (default: /etc/vlcp.conf)
  -d            Start as a daemon (Need python-daemon support)
  -p            When start as a daemon, specify a pid file (default: /var/run/vlcp.pid, or configured in
                configuration file)
  startmodule   Specify modules to be started, replace server.startup in configuration file
  -h,-?,--help  Show this help
'''
def usage():
    print(doc)
    sys.exit(2)
def parsearg():
    try:
        options, args = getopt.gnu_getopt(sys.argv[1:], 'f:p:?hd', 'help')
        configfile = None
        pidfile = '/var/run/vlcp.pid'
        daemon = False
        for k,v in options:
            if k == '--help' or k == '-?' or k == '-h':
                usage()
            elif k == '-f':
                configfile = v
            elif k == '-p':
                pidfile = v
            elif k == '-d':
                daemon = True
        startup = None
        if args:
            startup = args
        return (configfile, daemon, pidfile, startup)
    except getopt.GetoptError as exc:
        print(exc)
        usage()
        

if __name__ == '__main__':
    (config, daemon, pidfile, startup) = parsearg()
    if config is None:
        if os.path.isfile('/etc/vlcp.conf'):
            config = '/etc/vlcp.conf'
        else:
            print('/etc/vlcp.conf is not found; start without configurations.')
    elif not config:
        config = None
    main(config, startup, daemon, pidfile)
