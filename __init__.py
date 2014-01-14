# encoding: utf-8
import os
import string
import random
import re
import time
import datetime
from subprocess import Popen, PIPE

import bones.event
from bones.bot import Module
from twisted.internet import reactor

mod_dir = os.path.dirname(__file__)
arg_separator = ","
bot_admin = "KennethD"

def msg(event, string1, string2=False):
	prefix = "\x0312[KD]"
	if len(string1.strip("\n")) >= 1:
		if string2 != False:
			event.channel.msg(str(prefix + "\x0315" + string1 + "\x0300" + string2))
		else:
			event.channel.msg(str(prefix + "\x03 " + string1))
			
def error(event, string):
	errPrefix = "\x034[Error]\x03 "
	event.channel.msg(errPrefix + string)
	
def warn(event, string):
	warnPrefix = "\x038[Warning]\x03 "
	event.channel.msg(warnPrefix + string)
	
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
				warn(event, "No manual entry by that name.")
		else:
			warn(event, "Please specify a manual page.")
			
	@bones.event.handler(trigger="motd")
	@bones.event.handler(event=bones.event.UserJoinEvent)
	def motd(self, event, i=0):
		with open(os.path.join(mod_dir, "motd.txt"), "r") as motdfile:
			motd = motdfile.read()
		if len(motd) > 0:
			motd_lines = motd.split("\n")
			for line in motd_lines:
				msg(event, line)
				i =+ 1
				
class utils(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.ongoingPings = {}
		
	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="cc")
	def cmdCalc(self, event):
		maxLen = 275
		if not event.args:
			msg(event, "Please provide a equation")
		else:
			calc = Popen("bc", stdin=PIPE, stdout=PIPE)
			calc_input = "".join(event.args).lower()
			
			if "pi" in calc_input:
				calc_input = calc_input.replace("pi", "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
			if "c" in calc_input:
				calc_input = calc_input.replace("c", "299792458")
			if "mathias" in calc_input:
				calc_input = calc_input.replace("mathias", "666")
			
			result = "".join(calc.communicate("%s\n" % calc_input.replace(",", "."))[0].split('\\\n')).split("\n")
			for line in result:
				if len(line) > maxLen:
					warn(event, "Result too long for chat. Protip: Try http://wolframalpha.com")
				else:
					if line.rstrip("\n").isdigit():
						msg(event, "{0:,}".format(int(line)).replace(",", ","))
					else:
						msg(event, line)
						
	@bones.event.handler(trigger="pw")
	@bones.event.handler(trigger="password")
	def cmdPW(self, event):
		maxLen = 256
		tArgs = 16
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		rand = "".join(random.choice(chars) for x in range(tArgs))
		if len(event.args) > 0:
			if int(event.args[0]) > int(maxLen):
				warn(event, "Length must be a valid number between 1 and 256!")
			else:
				tArgs = int(event.args[0])
				tArgs = max(1, min(tArgs, maxLen))
				rand = "".join(random.choice(chars) for x in range(tArgs))
				event.user.notice('Here you go: %s' % rand)
		else:
			event.user.notice('Here you go: %s' % rand)
			
	@bones.event.handler(trigger="tg")
	@bones.event.handler(trigger="tg14")
	def timetoTG14(self, event):
		tg14_timeleft = datetime.timedelta(0,1397631600 - time.time())
		msg(event, "Det er\x039 " + str(tg14_timeleft.days) + "\x03 dager og\x039 " + str(tg14_timeleft.seconds/3600) + "\x03 timer til \x0312TG14\x03!")
		
	#@bones.event.handler(trigger="ccon") # Preparing Currency Converter.
	#def cmdCurrencyConvert(self, event):
	
	@bones.event.handler(trigger="bcon")
	@bones.event.handler(trigger="hex")
	@bones.event.handler(trigger="bin")
	@bones.event.handler(trigger="dec")
	def cmdBaseConverter(self, event):
		global out_dec, out_hex, out_bin, dec_input
		args = [arg.strip() for arg in " ".join(event.args).split(arg_separator)]
		if len(args) > 1:
			event.args = [arg.strip() for arg in args[0].split(" ")]
			
		TriggerEvent = event.match.group(2).lower()
		hex_chars = re.compile("[a-f*]", re.I)
		dec_chars = re.compile("[2-9*]", re.I)
		bin_chars = re.compile("[0-1*]", re.I)
		out_dec = []
		out_hex = []
		out_bin = []
		out_ascii = []
		dec_input = []
		
		if len(event.args) >= 1:
			if TriggerEvent == "hex":
				sourcebase = "16"
			elif TriggerEvent == "bin":
				sourcebase = "2"
			elif TriggerEvent == "dec":
				sourcebase = "10"
			else:
				if event.args[0].lower().startswith(("0x", "hex")):
					sourcebase = "16"
					if event.args[0].lower() == "hex":
						del event.args[0]
				elif event.args[0].lower().startswith(("0b", "bin")):
					sourcebase = "2"
					if event.args[0].lower() == "bin":
						del event.args[0]
				elif event.args[0].lower() == "dec":
					sourcebase = "10"
					del event.args[0]
					
				elif hex_chars.search("".join(event.args)):
					sourcebase = "16"
				elif dec_chars.search("".join(event.args)):
					sourcebase = "10"
				elif bin_chars.search("".join(event.args)):
					sourcebase = "2"
			try:
				for num in event.args:
					dec_input.append(int(num, int(sourcebase)))
				for num in dec_input:
					out_dec.append(str(num))
					out_hex.append(hex(num))
					out_bin.append(bin(num))
					if len(args) > 1:	
						if args[1].lower().startswith(("ascii", "txt")):
							out_ascii.append(hex(num).replace("0x", "").decode("hex"))
							
				dec_out = " ".join(out_dec)
				hex_out = " ".join(out_hex).replace("0x", "")
				if len("".join(out_bin)) > 128:
					decrease = len("".join(out_bin)) - 128
					string = " ".join(out_bin).replace("0b", "").replace('', '')[:-decrease].upper() + "..."
				else:
					string = " ".join(out_bin).replace("0b", "")
				bin_out = string
				
				if len(args) > 1:
					if args[1].lower().startswith(("dec", "10")):
						msg(event, "[Dec] ", dec_out)
					elif args[1].lower().startswith(("hex", "16")):
						msg(event, "[Hex] ", hex_out)
					elif args[1].lower().startswith(("bin", "2")):
						msg(event, "[Bin] ", bin_out)
					elif args[1].lower().startswith(("ascii", "txt")):
						msg(event, "[TXT] ", "".join(out_ascii))
					else:
						warn(event, "Unknown output")
				else:
					msg(event, "[Dec] ", dec_out)
					msg(event, "[Hex] ", hex_out)
					msg(event, "[Bin] ", bin_out)
			except ValueError:
				error(event, "Invalid number")
			except TypeError:
				error(event, "Invalid input")
		else:
			warn(event, "Usage: [Hex/Bin/Dec] Numbers to convert.")
			
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
			
class fun(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.danceCooldown = {}
		self.danceCooldownTime = None
	#	self.ongoingCount = False
	
	#@bones.event.handler(trigger="countdown")
	#def ny2k14(self, event):
	#	if self.ongoingCount == False:
	#		self.ongoingCount = True
	#		wait_time = 1388530800 - int(time.time())
	#		#wait_time = int(time.time() + 10) - int(time.time())
	#		reactor.callLater(wait_time, msg, event, "Godt Nyttår! \x039:D")
	#	else:
	#		warn(event, "Countdown already initiated!")
	
	@bones.event.handler(trigger="fortune")
	def cmdFortune(self, event, i=0):
		fortune = Popen("fortune", stdout=PIPE)
		fortune_lines = fortune.communicate()[0].split("\n")
		for line in fortune_lines:
			msg(event, line)
			i =+ 1
	
	@bones.event.handler(trigger="allo")
	def cmdAlloQuotes(self, event, i=0):
		inputfile = "allo"
		fortune = Popen(["fortune", os.path.join(mod_dir, "fortunes" , inputfile)], stdout=PIPE)
		allo_lines = fortune.communicate()[0].split("\n")
		for line in allo_lines:
			msg(event, line)
			i =+ 1
			
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
			if len(event.args) >=1:
				if len(args[0].strip(" ")) >= 1:
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
				msg(event, deathmessage)
				
	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def randomStringTriggers(self, event):
		msg = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if msg.startswith(":>") and event.user.nickname == bot_admin:
			event.channel.msg(":>")
			
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