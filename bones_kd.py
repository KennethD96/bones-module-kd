# -*- encoding: utf8 -*-
import string
import random
#import logging
#from datetime import datetime

from bones import event
from bones.bot import Module, urlopener


class utils(Module):

	def pwGen(size=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
		return ''.join(random.choice(chars) for x in range[size])

	@event.handler(trigger="pw")
	@event.handler(trigger="password")
	def cmdPW(self, event):
		event.client.msg(event.channel, "Here's your password: " % self.pwGen() )
