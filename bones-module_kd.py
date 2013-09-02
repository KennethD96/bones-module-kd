
import string
import random
#import logging
#from datetime import datetime

from bones import event
from bones.bot import Module, urlopener


class utils(Module):

	@event.handler(trigger="pw") # Sends a random password by notice
	@event.handler(trigger="password")
	def cmdPW(self, event):
		tArgs = 16
		if len(event.args) > 128:
			tArgs = 16
		elif len(event.args) > 0:
			tArgs = event.args[1]
		
		def pwGen(size=tArgs, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
			return ''.join(random.choice(chars) for x in range(size))
		event.client.notice(event.user.nickname, "Here you go: %s" % pwGen() )

	@event.handler(trigger="echo") # Used for debuging of tArgs
	def cmdEcho(self, event):
		targs = event.args[0]
		event.client.msg(event.channel, targs)
