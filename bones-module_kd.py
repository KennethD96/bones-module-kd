
import string
import random
#import logging
#from datetime import datetime

from bones import event
from bones.bot import Module

class utils(Module):

	@event.handler(trigger="pw") # Sends a random password by notice
	@event.handler(trigger="password")
	def cmdPW(self, event):
		tArgs = 16
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		
		if event.args[0].isdigit():
		
			if event.args[0] > 0:
				tArgs = int(event.args[0])
				if event.args[0] > 128:
					tArgs = 16

				gen = ''.join(random.choice(chars) for x in range(tArgs))
				pwGen = 'Here you go: %s' % gen
			
		else:
			pwGen = "Value must be a valid number between 1 and 128!"
		
		event.client.notice(event.user.nickname, pwGen )

	@event.handler(trigger="echo") # Used to debug tArgs
	def cmdEcho(self, event):
		event.client.msg(event.channel, " ".join(event.args)) 