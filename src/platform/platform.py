#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for interaction with the computers operating systems"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2021-10-10"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



import sys
import os # operating system dedicated builtin module
#import platform # sys module provide the needed os info and is already imported for other purposes
#import sysconfig # Provide access to Python’s configuration information
import getpass#a portable way to get the current user's username

### following modules allow to know the consumption and the functioning of python progs,
### this kind of task is useful while conceptioning,
### But should normally be options of a good IDE, 
### A good IDE should also allow to display the result in sortable column or in statistics graphs
#import cProfile,profile # provide statistics that describes how often and for how long various parts of the program executed.
#import trace # list functions executed during program run.
#import tracemalloc #a debug tool to trace memory blocks allocated by Python to the running program
#import resource # This module provides measuring and controlling system resources utilized by program.

### modules capable of changing the name of processes
##import procname # NOT available in Debian repository
##import prctl # NOT available for python3
import setproctitle# "set proc title" must be installed (available in Debian repository)



### platform constants names
PLATFORM_LINUX='linux'
PLATFORM_WINDOWS='win'
PLATFORM_UNKNOW='unknow'


def get_os_name():
	"""return the name of the current used operating system platform"""
	### can be used to detect the operating systems: os.name,os.uname(),sys.platform,platform.platform(),platform.system(),platform.system_alias(),platform.uname()
	### the operating system information should be also in the env variables, but its not certain
	if sys.platform.startswith(PLATFORM_LINUX):
		return PLATFORM_LINUX
	elif sys.platform.startswith(PLATFORM_WINDOWS):
		return PLATFORM_WINDOWS
	else :
		return PLATFORM_UNKNOW
	
def get_user_name():
	"""return user login name"""
	### LOGNAME is the original variable and tends to be used in System V Unix and its decendants.
	### USER was introduced by BSD to replace LOGNAME. These days lots of versions of Unix provide both in an effort to please everybody.
	### If both are present they should have the same value.
	#name=os.environ.get('USER')# when script run through sudo, "USER" is usually set to root
	#name=os.environ.get('LOGNAME')# and "USERNAME" is set with the user name running sudo.

	#name=os.getlogin() # with pipe raise OSError: Inappropriate ioctl for device
	name=getpass.getuser()# this function looks at the values of various environment variables to determine the user name.

	#print(name)
	return name

def get_shell_env():
	"""return all shell environment variables"""
	### os.getenv() is deprecated in favour of os.environ
	env= os.environ#.keys()
	#print(env)
	return env

def set_process_name(name):
	"""set process name"""
	#prctl.set_name(name)
	#prctl.set_proctitle(name)
	#print(prctl.get_name())
		
	setproctitle.setproctitle(name)
	#print(setproctitle.getproctitle())
