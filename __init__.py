# encoding: utf-8
import platform, socket
import string, random
import time, datetime

import bones.event, logging
from bones.bot import Module
from __main__ import *

class core(Module):

	@bones.event.handler(trigger="kdver")
	def return_ver(self, event):
		msg(event.channel.msg, "INFO", "%s \x0309%s \x0312(%s)" % 
		(
			module_name, module_version, module_date
		))
		if len(event.args) > 0:
			arg = event.args[0].lower()
			
			if arg == "debug":
				msg(event.channel.msg, "INFO", "System time:\x0309 %s" % (time.ctime()))
			if arg == "info" or arg == "debug":
				msg(event.channel.msg, "INFO", "Running \x0309%s %s\x0300 on \x0309%s" % 
				(
					platform.python_implementation(), platform.python_version(), platform.node()
				))
				msg(event.channel.msg, "INFO", "OS: \x0312%s %s" % (platform.system(), platform.release()))
