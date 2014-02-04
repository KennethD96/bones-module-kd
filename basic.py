# encoding: utf-8
import os

import bones.event, logging
from bones.bot import Module
from __main__ import *

class help(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)

	@bones.event.handler(trigger="help")
	@bones.event.handler(trigger="h")
	def cmdHelp(self, event):
		with open(os.path.join(etc_path, "help.txt"), "r") as helpfile:
			helpTxt = helpfile.read()
		msg(event.user.msg, helpTxt.rstrip("\n"))
		
	@bones.event.handler(trigger="man")
	def cmdMan(self, event):
		if event.args:
			manpage = event.args[0]
			manpath = os.path.join(etc_path, "man", manpage)
			if os.path.exists(manpath):
				with open(os.path.join(manpath)) as manfile:
					manpage = manfile.read()
					msg(event.user.msg, manpage.rstrip("\n"))
			else:
				warn(event, "No manual entry by that name.")
		else:
			warn(event, "Please specify a manual page.")

class misc(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
			
	@bones.event.handler(trigger="motd")
	@bones.event.handler(event=bones.event.UserJoinEvent)
	def motd(self, event):
		with open(os.path.join(etc_path, "motd.txt"), "r") as motdfile:
			motd = motdfile.read()
		if len(motd) > 0:
			motd_lines = motd.split("\n")
			for line in motd_lines:
				msg(event.channel.msg, line)