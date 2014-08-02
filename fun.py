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

	@bones.event.handler(trigger="magic8")
	@bones.event.handler(trigger="8ball")
	def magic8(self, event):
		magic8_path = os.path.join(etc_path, "magic8.txt")
		question = " ".join(event.args)
		if re.match(".+[?|？|؟|՞|;|;]\s*$", question):
			if os.path.exists(magic8_path):
				with open(magic8_path, "r") as responses_file:
					responses = responses_file.read().split("\n")
					magic8_response = random.choice(responses)
					while magic8_response == "":
						magic8_response = random.choice(responses)
					msg(event.channel.msg, "8-Ball", "\x03" + magic8_response)
		else:
			msg(event.channel.
				msg, "8-Ball", "Please give me a question.")

class responses(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.danceCooldown = {}
		self.danceCooldownTime = None
		self.privileged_users = ["KennethD", "_404`d", "Mathias"] # Users applicable for responses in the privileged_responses dictionary.
		self.privileged_responses = {} # Contains a dictionary of responses available for privileged users only.
		self.randomresponses = {} # Contains a dictionary of responses available to all users.
				
	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def stringResponses(self, event):
		msg_str = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		for trigger, response in self.randomresponses.iteritems():
			if msg_str.startswith(trigger):
				event.channel.msg(response)
		for trigger, response in self.privileged_responses.iteritems():
			if msg_str.startswith(trigger) and event.user.nickname in self.privileged_users:
				event.channel.msg(response)