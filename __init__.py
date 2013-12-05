# encoding: utf-8
import os
import string
import random
import re
import time

from subprocess import Popen, PIPE
from datetime import datetime

#import logging
import bones.event
from bones.bot import Module
from twisted.internet import reactor

mod_dir = os.path.dirname(__file__)
antiflood_timeout = 2.0

class basic(Module):

	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.motdOnUserJoin = True

	@bones.event.handler(trigger="help")
	@bones.event.handler(trigger="h")
	def cmdHelp(self, event):
		with open(os.path.join(mod_dir, "help.txt"), "r") as helpfile:
			helpTxt = helpfile.read()
		event.user.msg(helpTxt.rstrip("\n"))

	@bones.event.handler(trigger="man")
	def cmdMan(self, event):
		if event.args:
			manpage = event.args[0]
			manpath = os.path.join(mod_dir, "man", manpage)
			if os.path.exists(manpath):
				with open(os.path.join(manpath)) as manfile:
					manpage = manfile.read()
					event.user.msg(manpage.rstrip("\n"))
			else:
				event.channel.msg("No manual entry by that name.")
		else:
			event.channel.msg("Please specify a manual page.")



	@bones.event.handler(trigger="motd")
	@bones.event.handler(event=bones.event.UserJoinEvent)
	def motd(self, event, i=0):
		with open(os.path.join(mod_dir, "motd.txt"), "r") as motdfile:
			motd = motdfile.read()
		if len(motd) > 0:
			motd_lines = motd.split("\n")
			for line in motd_lines:
				event.channel.msg(line)
				i =+ 1
				#time.sleep(antiflood_timeout)
		else:
			return

class utils(Module):

	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="cc")
	@bones.event.handler(trigger="c")
	@bones.event.handler(trigger="bc")
	def cmdCalc(self, event):
		maxLen = 512
		if not event.args:
			event.channel.msg("Please provide a equation")
		else:
			formula = "".join(event.args)
			calc = Popen("bc", stdin=PIPE, stdout=PIPE)
			result = "".join(calc.communicate("%s\n" % formula.replace(",", "."))[0].split('\\\n'))
			if len(result) > maxLen:
				event.channel.msg("Result too long for chat. Protip: Try http://wolframalpha.com")
			else:
				if result.rstrip("\n").isdigit():
					event.channel.msg("{0:,}".format(int(result)).replace(",", ","))
				else:
					event.channel.msg(result)

	@bones.event.handler(trigger="pw")
	@bones.event.handler(trigger="password")
	@bones.event.handler(trigger="random")
	def cmdPW(self, event):
		maxLen = 256
		tArgs = 16
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		rand = "".join(random.choice(chars) for x in range(tArgs))
		if len(event.args) > 0:
			if int(event.args[0]) > int(maxLen):
				event.channel.msg("Length must be a valid number between 1 and 256!")
			else:
				tArgs = int(event.args[0])
				tArgs = max(1, min(tArgs, maxLen))
				rand = "".join(random.choice(chars) for x in range(tArgs))
				event.user.notice('Here you go: %s' % rand)
		else:
			event.user.notice('Here you go: %s' % rand)

	@bones.event.handler(trigger="ping")
	def cmdPing(self, event):
		nick = event.user.nickname
		if nick not in self.ongoingPings:
			self.ongoingPings[nick] = event.channel.name
			event.user.ping()
		else:
			event.user.notice("Please wait until your ongoing ping in %s is finished until trying again." % self.ongoingPings[nick])

	@bones.event.handler(event=bones.event.CTCPPongEvent)
	def eventPingResponseReceive(self, event):
		nick = event.user.nickname
		if nick in self.ongoingPings:
			event.user.notice("%s: Your response time was %.3f seconds." % (nick, event.secs))
			del self.ongoingPings[nick]

	#@event.handler(trigger="echo") # Provided for debuging purposes.
	#def cmdEcho(self, event):
	#	event.channel.msg(" ".join(event.args))

	#class converters(Module):

		#@bones.event.handler(trigger="ccon") # Preparing Currency Converter.
		#def cmdCurrencyConvert(self, event):
		#	return

	@bones.event.handler(trigger="basecon")
	@bones.event.handler(trigger="bcon")
	def cmdBaseConverter(self, event):
		global out_dec, out_hex, out_bin, dec_input
		out_dec = []
		out_hex = []
		out_bin = []
		dec_input = []

		if len(event.args) >= 1:
			if event.args[0].lower().startswith(("0x", "hex")):
				sourcebase = "hex"
				if event.args[0].lower() == "hex":
					del event.args[0]
			
			elif event.args[0].lower().startswith(("0b", "bin")):
				sourcebase = "bin"
				if event.args[0].lower() == "bin":
					del event.args[0]
			
			elif event.args[0].lower() == "dec":
				sourcebase = "dec"
				del event.args[0]
			
			else:
				sourcebase = "dec"

			def convert():
				for item in dec_input:
					out_dec.append(str(item))
					out_hex.append(hex(item))
					out_bin.append(bin(item))

			if "hex" in sourcebase:
				for item in event.args:
					dec_input.append(int(item, 16))
				convert()
			
			elif "bin" in sourcebase:
				for item in event.args:
					dec_input.append(int(item, 2))
				convert()
			
			elif "dec" in sourcebase:
				for item in event.args:
					dec_input.append(int(item))
				convert()

			event.channel.msg("Dec: " + " ".join(out_dec))
			#reactor.callLater(antiflood_timeout)
			event.channel.msg("Hex: " + " ".join(out_hex).replace("0x", ""))
			#reactor.callLater(antiflood_timeout)
			event.channel.msg("Bin: " + " ".join(out_bin).replace("0b", ""))
		else:
			event.channel.msg("Usage: [Hex/Bin/Dec] Numbers to convert.")


class fun(Module):

	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)

		self.danceCooldown = {}
		self.danceCooldownTime = None

	@bones.event.handler(trigger="fortune")
	def cmdFortune(self, event, i=0):
		fortune = Popen("fortune", stdout=PIPE)
		fortune_lines = fortune.communicate()[0].split("\n")
		for line in fortune_lines:
			event.channel.msg(line)
			i =+ 1
			#time.sleep(antiflood_timeout)
	
	@bones.event.handler(trigger="allo")
	def cmdAlloQuotes(self, event, i=0):
		inputfile = "allo"
		fortune = Popen(["fortune", os.path.join(mod_dir, "fortunes" , inputfile)], stdout=PIPE)
		allo_lines = fortune.communicate()[0].split("\n")
		for line in allo_lines:
			event.channel.msg(line)
			i =+ 1
			#time.sleep(antiflood_timeout)

	@bones.event.handler(trigger="killstreak")
	@bones.event.handler(trigger="kill")
	def cmdKillstreak(self, event):
			args = [arg.strip() for arg in " ".join(event.args).split(",")]
			target = event.user.nickname
			player = random.choice(event.channel.users).nickname
			materials = ["Wooden", "Stone", "Iron", "Golden", "Diamond"]
			tools = ["Sword", "Pickaxe", "Axe"]
			other = ["Diretide", "ahue"]
			weapons = [random.choice(materials) + " " + random.choice(tools), random.choice(other)]
			messagefiles = ["deathmessages.txt", "deathmessages_weapons.txt"]
			if len(event.args) >=1:
				target = args[0]
				if target != event.user.nickname:
					player = event.user.nickname
				if len(args) >= 2:
					if len(args[1]) >= 1:
						messagefiles = ["deathmessages_weapons.txt"]
						weapons = [args[1]]
			with open(os.path.join(mod_dir, "deathmessages", random.choice(messagefiles)), "r") as deathmessages:
				deathmessage = random.choice(deathmessages.readlines())
				if "[target]" in deathmessage:
					deathmessage = deathmessage.replace("[target]", target)
				if "[player]" in deathmessage:
					deathmessage = deathmessage.replace("[player]", player)
				if "[weapon]" in deathmessage:
					deathmessage = deathmessage.replace("[weapon]", random.choice(weapons))
				event.channel.msg(deathmessage)

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