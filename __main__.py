# encoding: utf-8
import logging
import os

MODULE_NAME = "BONES-MODULE-KD_ESSENTIALS"
MODULE_VERSION = "v0.1.1-DEV"
MODULE_DATE = "07. Jul 2015 20:32 UTC"

MOD_PATH = os.path.dirname(__file__)
ETC_PATH = MOD_PATH + "/etc/"
CACHE_PATH = MOD_PATH + "/cache/"

ARG_SEPARATOR = ","

logger = logging.getLogger(MODULE_NAME)


def msg(event, string1, string2=False, prefix="\x0312[KD]"):
    """If string2 is supplied string1 will be
    used as a prefix for the output.
    Note that empty lines will be ignored.
    Use a space if you need a empty line."""
    if len(string1.strip("\n")) >= 1:
        if string2 is not False:
            for line in string2.split("\n"):
                if len(line) != 0:
                    event("%s\x0315[%s\x0315]\x0F %s" % (
                        prefix, string1, line))
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
