# encoding: utf-8

module_name = "BONES-MODULE-KD_ESSENTIALS"
module_version = "v0.0.2-DEV"
module_date = "14. Jan 2015 08:50 CET"

import os, sys
import string, random
import time, datetime

import bones.event, logging
from bones.bot import Module, urlopener

mod_path = os.path.dirname(__file__)
etc_path = mod_path + "/etc/"
cache_path = mod_path + "/cache/"

arg_separator = ","

today = datetime.datetime.today()
logger = logging.getLogger(module_name)

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
                    event("%s\x0315[%s\x0315]\x0F %s" %
                        (prefix, string1, line))
        else:
            for line in string1.split("\n"):
                if len(line) != 0:
                    event("%s\x0F %s" % (prefix, line))

def error(event, string):
    errPrefix = "\x034[Error]\x0F "
    for line in string.split("\n"):
        event(errPrefix + line)

def warn(event, string):
    warnPrefix = "\x038[Warning]\x0F "
    for line in string.split("\n"):
        event(warnPrefix + line)
