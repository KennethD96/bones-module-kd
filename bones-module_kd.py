 # encoding: utf-8
import string
import random
import re

from subprocess import Popen, PIPE
from datetime import datetime

#import logging
import bones.event
from bones.bot import Module
from twisted.internet import reactor

class utils(Module):

	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.ongoingPings = {}

	@bones.event.handler(trigger="help")
	@bones.event.handler(trigger="h")
	def cmdHelp(self, event, i=0):
		with open("help.txt", "r") as helpfile:
			helpFile = helpfile.read()
		helpfile.closed
		help_lines = helpFile.split("\n")
		for line in help_lines:
			reactor.callLater(i*0.2, event.channel.msg, line)
			i =+ 1

	@bones.event.handler(trigger="motd")
	@bones.event.handler(event=bones.event.UserJoinEvent)
	def motd(self, event, i=0):
		with open("motd.txt", "r") as motdfile:
			motd = motdfile.read()
		motdfile.closed
		if len(motd) > 0:
			motd_lines = motd.split("\n")
			for line in motd_lines:
				reactor.callLater(i*0.2, event.channel.msg, line)
				i =+ 1
		else:
			return

	@bones.event.handler(trigger="pw") # Sends a random password by notice
	@bones.event.handler(trigger="password")
	@bones.event.handler(trigger="random")
	def cmdPW(self, event):
		maxLen = 256
		tArgs = 16
		args = "".join(event.args)
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		rand = "".join(random.choice(chars) for x in range(tArgs))
		if len(event.args) > 0:
			if int(event.args) > maxLen:
				event.channel.msg("Length must be a valid number between 1 and 256!")
			else:
				tArgs = int(event.args[0])
				tArgs = max(1, min(tArgs, maxLen))
				rand = "".join(random.choice(chars) for x in range(tArgs))
				event.user.notice('Here you go: %s' % rand)
		else:
			event.user.notice('Here you go: %s' % rand)

	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="cc")
	@bones.event.handler(trigger="c")
	def cmdCalc(self, event):
		maxLen = 512
		if not event.args:
			event.channel.msg("Please provide a equation")
		else:
			formula = "".join(event.args)
			calc = Popen("bc", stdin=PIPE, stdout=PIPE)
			result = "".join(calc.communicate("%s\n" % formula)[0].split('\\\n'))
			if len(result) > maxLen:
				event.channel.msg("Result too long for chat.")
			else:
				if result.rstrip("\n").isdigit():
					event.channel.msg("{0:,}".format(int(result)).replace(",", "'"))
				else:
					event.channel.msg(result)

	@bones.event.handler(trigger="ping")
	def cmdPing(self, event):
		nick = event.user.nickname
		if nick not in self.ongoingPings:
			self.ongoingPings[nick] = event.channel
			event.client.ping(nick)
		else:
			event.user.notice("Please wait until your ongoing ping in %s is finished until trying again." % self.ongoingPings[nick])

	@bones.event.handler(event="CTCPPong")
	def eventPingResponseReceive(self, event):
		nick = event.user.nickname
		if nick in self.ongoingPings:
			channel = self.ongoingPings[nick]
			event.channel.msg("%s: Your response time was %.3f seconds." % (nick, event.secs))
			del self.ongoingPings[nick]

	#@event.handler(trigger="echo") # Provided for debuging purposes.
	#def cmdEcho(self, event):
	#	event.channel.msg(" ".join(event.args))

class fun(Module):

	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)

		self.danceCooldown = {}
		self.danceCooldownTime = None

	@bones.event.handler(trigger="fortune") # Calls the UNIX "fortune" application and sends the output to the channel
	def cmdFortune(self, event, i=0):
		fortune = Popen("fortune", stdout=PIPE)
		fortune_lines = fortune.communicate()[0].split("\n")
		for line in fortune_lines:
			reactor.callLater(i*0.2, event.channel.msg, line)
			i =+ 1
	
	@bones.event.handler(trigger="allo") # Same as above just using a different input file
	def cmdFortune(self, event, i=0):
		inputfile = "allo"
		fortune = Popen(["fortune", inputfile], stdout=PIPE)
		lines = fortune.communicate()[0].split("\n")
		for line in lines:
			reactor.callLater(i*0.2, event.channel.msg, line)
			i =+ 1
		

	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def DANCE(self, event, step=0):
		msg = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if "DANCE" in msg:
			if not self.danceCooldownTime:
				self.danceCooldownTime = int(self.settings.get("module.UselessResponses", "dance.cooldown"))
			if step == 0:
				if event.channel.name in self.danceCooldown:
					last = self.danceCooldown[event.channel.name]
					now = datetime.utcnow()
					delta = now - last
					if delta.seconds < self.danceCooldownTime:
						wait = self.danceCooldownTime - delta.seconds
						event.user.notice("Please wait %s more seconds." % wait)
						return
				self.danceCooldown[event.channel.name] = datetime.utcnow()
				event.client.ctcpMakeQuery(event.channel.name, [('ACTION', "dances")])
				reactor.callLater(1.5, self.DANCE, event, step=1)
			elif step == 1:
				event.channel.msg(r":D\-<")
				reactor.callLater(1.0, self.DANCE, event, step=2)
			elif step == 2:
				event.channel.msg(r":D|-<")
				reactor.callLater(1.0, self.DANCE, event, step=3)
			elif step == 3:
				event.channel.msg(r":D/-<")
				reactor.callLater(1.0, self.DANCE, event, step=4)
			elif step == 4:
				event.channel.msg(r":D)-<")
