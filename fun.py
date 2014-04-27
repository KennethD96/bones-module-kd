# encoding: utf-8
import os
import string, re
import time, datetime
from subprocess import Popen, PIPE

import bones.event, logging
from bones.bot import Module
from twisted.internet import reactor
from __main__ import *

class triggers(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
	
	@bones.event.handler(trigger="fortune")
	def cmdFortune(self, event):
		try:
			fortune = Popen("fortune", stdout=PIPE)
			fortune_lines = fortune.communicate()[0].split("\n")
			for line in fortune_lines:
				msg(event.channel.msg, line)
		except OSError:
			logger.error("Could not fetch Fortune, is it installed?")
		
	@bones.event.handler(trigger="allo")
	def cmdAlloQuotes(self, event):
		try:
			inputfile = "allo"
			fortune = Popen(["fortune", os.path.join(etc_path, "fortunes" , inputfile)], stdout=PIPE)
			allo_lines = fortune.communicate()[0].split("\n")
			for line in allo_lines:
				msg(event.channel.msg, line)
		except OSError:
			logger.error("Could not fetch Fortune, is it installed?")
		
	@bones.event.handler(trigger="killstreak")
	@bones.event.handler(trigger="kill")
	def cmdKillstreak(self, event):
			args = [arg.strip() for arg in " ".join(event.args).split(arg_separator)]
			target = event.user.nickname
			player = random.choice(event.channel.users).nickname
			
			materials = ["Wooden", "Stone", "Iron", "Golden", "Diamond"]
			tools = ["Sword", "Pickaxe", "Axe"]
			other = ["Diretide", "ahue", "Java™"]
			weapons = [random.choice(materials) + " " + random.choice(tools), random.choice(other)]
			messagefiles = ["deathmessages.txt", "deathmessages_weapons.txt"]
			if len(event.args) >= 1:
				if len(args[0].strip(" ")) >= 1:
					target = args[0]
				if target != event.user.nickname:
					player = event.user.nickname
				if len(args) >= 2:
					if len(args[1]) >= 1:
						messagefiles = ["deathmessages_weapons.txt"]
						weapons = [args[1]]
			target, player, weapon = (
				"\x0304" + target + "\x03",
				"\x0304" + player + "\x03",
				"\x0305" + random.choice(weapons) + "\x03",
			)
			with open(os.path.join(etc_path, "deathmessages", random.choice(messagefiles)), "r") as deathmessages:
				deathmessage = random.choice(deathmessages.readlines())
				if "[target]" in deathmessage:
					deathmessage = deathmessage.replace("[target]", target)
				if "[player]" in deathmessage:
					deathmessage = deathmessage.replace("[player]", player)
				if "[weapon]" in deathmessage:
					deathmessage = deathmessage.replace("[weapon]", weapon)
				msg(event.channel.msg, deathmessage)

class responses(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.danceCooldown = {}
		self.danceCooldownTime = None
		self.privileged_users = ["KennethD", "_404`d", "Mathias"]
		self.privileged_responses = {
		}
		self.randomresponses = {}
				
	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def stringResponses(self, event):
		msg_str = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		for trigger, response in self.randomresponses.iteritems():
			if msg_str.startswith(trigger):
				event.channel.msg(response)
		for trigger, response in self.privileged_responses.iteritems():
			if msg_str.startswith(trigger) and event.user.nickname in self.privileged_users:
				event.channel.msg(response)

	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def DANCE(self, event, step=0):
		msg = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if "DANCE" in msg:
			if not self.danceCooldownTime:
				self.danceCooldownTime = int(self.settings.get("module.UselessResponses", "dance.cooldown"))
			if step == 0:
				if event.channel.name in self.danceCooldown:
					last = self.danceCooldown[event.channel.name]
					now = datetime.datetime.utcnow()
					delta = now - last
					if delta.seconds < self.danceCooldownTime:
						wait = self.danceCooldownTime - delta.seconds
						event.user.notice("Please wait %s more seconds." % wait)
						return
				self.danceCooldown[event.channel.name] = datetime.datetime.utcnow()
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