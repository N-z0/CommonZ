#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "All progs have the need to output some messages,This module will provide many options for output prog's messages."#information describing the purpose of this modul
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "v4.1.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact address for more info about this file



### log messages are just in simple English to :
###   be able displayed without problem in any type of terminal,
###   be able to be understood by an administrator consulting the logs
###   facilitate world research and share logs on the Internet



### import the required modules
import sys # use for stderr

#import reprlib # print python objects with better representation.
#import pprint # print python objects with a many lines format.
#import textwrap # formats paragraphs of text to fit on a screen of a given width
#import readline # makes easier to read/write history files and completion

#import traceback #exactly mimics the behavior of the Python interpreter when it prints a stack trace.

#import warnings #  derived from the built-in Exception class , (If capture is True, warnings issued by the warnings module will be redirected to the logging system.)

#import syslog # only allow to send logs to SyslogD
###	LOG_EMERG		Emergency			System unusable
###	LOG_ALERT		Alert				Immediate intervention is necessary.
###	LOG_CRIT		Critical 			Critical error for the system.
###	LOG_ERR			Error				Operating error.
###	LOG_WARNING		Warning				an error can occur if no action is taken
###	LOG_NOTICE		Notice				Normal event worth reporting.
###	LOG_INFO		Informational			For more information.
###	LOG_DEBUG		Debugging			Debugging message.
###Log options:
###	LOG_CONS		if there is an error during the transmission write directly to the system console
###	LOG_NDELAY	Open the connection immediately (normally, the connection is open when the first message is sent).
###	LOG_NOWAIT	Do not wait for the end of the child process. The glibc library does not create child process, so this option has no effect on Linux.
###	LOG_ODELAY	The reverse of LOG_NDELAY; opening connection is delayed until the first invocation of syslog. This is the default behavior
###	LOG_PERROR	(not in POSIX.1-2001) write also on stderr.
###	LOG_PID			write PID in all messages.
#syslog.openlog(sys.argv[0],syslog.LOG_CONS|syslog.LOG_PERROR,syslog.LOG_USER) # syslog.openlog([ident[, log_option[, facility]]])
#syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_INFO))# set logs level ,Log messages which are less severe will be ignored
#syslog.syslog(syslog.LOG_DEBUG,'start')
#syslog.syslog(syslog.LOG_WARNING,"this program was designed for Linux operating system"+sys.platform )
#syslog.closelog()

import logging # logs system offering many options for logs output : file,syslog,terminal,etc,
from logging import handlers



### the following part is executed only one time even if this module is imported many times

### lastResort is used to handle logging events in the absence of any logging configuration.
### The end result is to just print the message to sys.stderr.
### This replaces the earlier error message saying that “no handlers could be found for logger XYZ”.
### If you need the earlier behaviour for some reason, lastResort can be set to None.
#logging.lastResort=None

### by default the root logger is used
logger = logging.getLogger()
### set the root logger not effective
### then by default any external module library will not be able to send messages trough the root logger
logger.addHandler(logging.NullHandler())
### default log level is logging.WARNING so need to change it.
### logging.NOTSET which causes all messages to be processed when the logger is the root logger,
logger.setLevel(logging.NOTSET)

### this can be loaded with file lines used for logs messages
### at index 0 a none message is always stored (for matching file line number and log index)
messages={'':('',)}



def setup(progname,logfile=None,syslog_verbosity=0,terminal_verbosity=0,logfile_verbosity=0):
	"""define what type of messages will be logged and how"""
	global logger
	### get a logger and set log system
	### if progname=None the root logger is used
	logger = logging.getLogger(progname)
	#logging.basicConfig(filename='example.log',level=logging.DEBUG)
	### default log level is logging.WARNING so need to change it.
	### logging.NOTSET which causes all messages to be processed when the logger is the root logger,
	### or delegation to the parent when the logger is a non-root logger.
	logger.setLevel(logging.DEBUG)
	### set level for each output system
	if syslog_verbosity==0 and terminal_verbosity==0 and logfile_verbosity==0 :
		### if all verbosity are at zero, all logs are ignored
		nh = logging.NullHandler()
		logger.addHandler(nh)
	else :
		logging_levels=(None,logging.CRITICAL,logging.ERROR,logging.WARNING,logging.INFO,logging.DEBUG,logging.NOTSET)
		if syslog_verbosity>0 :
			### logs go on syslog
			sh = handlers.SysLogHandler(address='/dev/log')#If not specified localhost:514 is used. Better than system dependent /dev/log on Linux /var/run/syslog on OS/X
			sh.setFormatter( logging.Formatter("{} %(message)s".format(progname)) )
			sh.setLevel(logging_levels[syslog_verbosity])
			logger.addHandler(sh)
		if terminal_verbosity>0 :
			### logs go on stderr terminal
			th = logging.StreamHandler(sys.stderr)
			th.setFormatter( logging.Formatter("【%(levelname)s】:%(message)s") )
			th.setLevel(logging_levels[terminal_verbosity])
			logger.addHandler(th)
		if logfile_verbosity>0 :
			### logs go on logfile
			### the logfile is deleted at each start, good for limit the file size,and reducing time for auditing the logs.
			### (still possible to do backup but Syslog is better for keeping logs a longtime)
			fh = logging.FileHandler(logfile,mode='w',encoding='utf-8',delay=False)
			fh.setFormatter( logging.Formatter('%(created)0.3f\t%(levelname)s\t%(message)s') )
			fh.setLevel(logging_levels[logfile_verbosity])
			logger.addHandler(fh)


def load_messages(pathname,context=''):
	"""load messages from .txt file lines"""
	global messages
	with open(pathname,'r') as txt_file:
		### at index 0 a none message is always stored
		messages[context]=tuple(['']+[line.strip() for line in txt_file])


def log_debug(index,data=(),context=''):
	"""log a debug level message"""
	log=messages[context][index].format(*data)
	logger.debug(log)
def log_info(index,data=(),context=''):
	"""log a info level message"""
	log=messages[context][index].format(*data)
	logger.info(log)
def log_warning(index,data=(),context=''):
	"""log a warning level message"""
	log=messages[context][index].format(*data)
	logger.warning(log)
def log_error(index,data=(),context=''):
	"""log a error level message"""
	log=messages[context][index].format(*data)
	logger.error(log)
def log_critical(index,data=(),context=''):
	"""log a critical level message"""
	log=messages[context][index].format(*data)
	logger.critical(log)


def shutdown():
	"""perform logging system shutdown"""
	### normally there’s no need to call this function
	### even without the logging module will shutdown
	logging.shutdown()
