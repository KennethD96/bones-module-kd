
import string
import random
import re
from subprocess import Popen, PIPE
from datetime import datetime
from twisted.internet import reactor
#import logging
#from datetime import datetime

import bones.event
from bones.bot import Module

class utils(Module):

	@bones.event.handler(trigger="pw") # Sends a random password by notice
	@bones.event.handler(trigger="password")
	@bones.event.handler(trigger="random")
	def cmdPW(self, event):
		tArgs = 16
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		if len(event.args) > 0:
			if len(event.args) > 256:
				event.client.notice(event.user.nickname, "Value must be a valid number between 1 and 256!")
				return
			else:
				tArgs = int(event.args[0])
				tArgs = max(1, min(tArgs, 256))
		
		rand = ''.join(random.choice(chars) for x in range(tArgs))
		event.client.notice(event.user.nickname, 'Here you go: %s' % rand)

	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="clc")
	@bones.event.handler(trigger="c")
	def cmdCalc(self, event):
		formula = "".join(event.args)
		calc = Popen("bc", stdin=PIPE, stdout=PIPE)
		result = "".join(calc.communicate("%s\n" % formula)[0].split('\\\n'))
		if not event.args:
			event.client.msg(event.channel, "You must specify a formula")
		else:
			if result.isdigit:
				event.client.msg(event.channel,"{0:,}".format(int(result)))
			else:
				event.client.msg(event.channel, result)

	#@event.handler(trigger="echo") # Provided for debuging purposes.
	#def cmdEcho(self, event):
	#	event.client.msg(event.channel, " ".join(event.args))

class fun(Module):

	@bones.event.handler(trigger="fortune") # Calls the UNIX "fortune" application and sends the output to the channel
	def cmdFortune(self, event, i=0):
		fortune = Popen("fortune", stdout=PIPE)
		lines = fortune.communicate()[0].split("\n")
		for line in lines:
			reactor.callLater(i*0.2, event.client.msg, event.channel, line)
			i =+ 1
	
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)

		self.danceCooldown = {}
		self.danceCooldownTime = None
		
	@bones.event.handler(event="Privmsg")
	def DANCE(self, event, step=0):
		msg = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if "DANCE" in msg:
			if not self.danceCooldownTime:
				self.danceCooldownTime = int(self.settings.get("module.UselessResponses", "dance.cooldown"))
			if step == 0:
				if event.channel in self.danceCooldown:
					last = self.danceCooldown[event.channel]
					now = datetime.utcnow()
					delta = now - last
					if delta.seconds < self.danceCooldownTime:
						wait = self.danceCooldownTime - delta.seconds
						event.client.notice(event.user.nickname, "Please wait %s more seconds." % wait)
						return
				self.danceCooldown[event.channel] = datetime.utcnow()
				event.client.ctcpMakeQuery(event.channel, [('ACTION', "dances")])
				reactor.callLater(1.5, self.DANCE, event, step=1)
			elif step == 1:
				event.client.msg(event.channel, r":D\-<")
				reactor.callLater(1.0, self.DANCE, event, step=2)
			elif step == 2:
				event.client.msg(event.channel, r":D|-<")
				reactor.callLater(1.0, self.DANCE, event, step=3)
			elif step == 3:
				event.client.msg(event.channel, r":D/-<")
				reactor.callLater(1.5, self.DANCE, event, step=4)
			elif step == 4:
				event.client.msg(event.channel, r":D)-<")
