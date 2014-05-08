# encoding: utf-8

module_name = "BONES-MODULE-KD_ESSENTIALS"
module_version = "v0.0.2-DEV"
module_date = "8.May 2014 08:19"

import os, sys
import string, random
import time, datetime

import bones.event, logging
from bones.bot import Module, urlopener
from bones.config import BaseConfiguration

mod_path = os.path.dirname(__file__)
etc_path = mod_path + "/etc/"
cache_path = mod_path + "/cache/"

arg_separator = ","

settings = BaseConfiguration(sys.argv[1])
today = datetime.datetime.today()
logger = logging.getLogger(module_name)
prefixChars = settings.get("bot", "triggerPrefixes").decode("utf-8")

def msg(event, string1, string2=False):
	"""If string2 is supplied string1 will be
	used as a prefix for the output.
	Note that empty lines will be ignored.
	Use a space if you need a empty line."""
	prefix = "\x0312[KD]"
	if len(string1.strip("\n")) >= 1:
		if string2 != False:
			for line in string2.split("\n"):
				if len(line) != 0:
					event("%s\x0315[%s\x0315]\x03 %s" % 
						(prefix, string1, line))
		else:
			for line in string1.split("\n"):
				if len(line) != 0:
					event("%s\x03 %s" % (prefix, line))

def error(event, string):
	errPrefix = "\x034[Error]\x03 "
	for line in string.split("\n"):
		event(errPrefix + line)
	
def warn(event, string):
	warnPrefix = "\x038[Warning]\x03 "
	for line in string.split("\n"):
		event(warnPrefix + line)