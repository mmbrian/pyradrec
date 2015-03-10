#!/usr/bin/env /usr/local/bin/python2.7

import os, shutil, time, random
from settings import APP_ROOT

# This is only basic logging on a text file

log_file = os.path.join(APP_ROOT, "log.log")

def log(msg):
	curr = time.gmtime()
	f = open(log_file, 'a')
	f.write("[%s:%s:%s GMT] " % (curr.tm_hour, curr.tm_min, curr.tm_sec))
	f.write(msg + "\n")
	f.flush()
	f.close()

def clear_logs():
	if os.path.exists(log_file):
		curr = time.gmtime()
		logs_dir = os.path.join(APP_ROOT, 'logs')
		if not os.path.exists(logs_dir): os.makedirs(logs_dir)
		backup = "logs/%s%s%s-%s%s%s-%s.log" % (curr.tm_year, curr.tm_mon, curr.tm_mday, \
								curr.tm_hour, curr.tm_min, curr.tm_sec, \
								random.randint(1, 100)) 
		shutil.copyfile(log_file, os.path.join(APP_ROOT, backup))
		os.remove(log_file)
	