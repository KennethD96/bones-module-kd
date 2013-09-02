
import string
import random
#import logging
#from datetime import datetime

from bones import event
from bones.bot import Module, urlopener


class utils(Module):

	@event.handler(trigger="pw")
	@event.handler(trigger="password")
	def cmdPW(self, event):
		targs = 16
		if len(event.args) > 0:
			targs = event.args[1]
		def pwGen(size=targs, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
			return ''.join(random.choice(chars) for x in range(size))
		event.client.notice(event.user.nickname, "Here you go: %s" % pwGen() )
