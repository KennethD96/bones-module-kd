# encoding: utf-8
import os

from bones.bot import Module
from __main__ import *
import bones.event


class help(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)

    @bones.event.handler(trigger="help")
    @bones.event.handler(trigger="h")
    def cmdHelp(self, event):
        with open(os.path.join(ETC_PATH, "help.txt"), "r") as helpfile:
            helpTxt = helpfile.read()
        msg(event.user.msg, helpTxt.rstrip("\n"))

    @bones.event.handler(trigger="man")
    def cmdMan(self, event):
        if event.args:
            manpage = event.args[0].lower()
            manpath = os.path.join(ETC_PATH, "man", manpage)
            if os.path.exists(manpath):
                with open(os.path.join(manpath)) as manfile:
                    manpage = manfile.read()
                    msg(event.user.msg, manpage.rstrip("\n"))
            else:
                warn(event.channel.msg, "No manual entry by that name.")
        else:
            warn(event.channel.msg, "Please specify a manual page.")


class misc(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)

    @bones.event.handler(trigger="motd")
    @bones.event.handler(event=bones.event.UserJoinEvent)
    def motd(self, event):
        with open(os.path.join(ETC_PATH, "motd.txt"), "r") as motdfile:
            motd = motdfile.read()
        if len(motd) > 0:
            motd_lines = motd.split("\n")
            for line in motd_lines:
                if "%c" in line:
                    line = line.replace("%c", "\x03")
                msg(event.channel.msg, line)
