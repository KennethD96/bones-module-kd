# encoding: utf-8
import os
import string, random, re
import time, datetime
try:
	import pytz
	pytz_available = True
except ImportError:
	pytz_available = False

import urllib
from subprocess import Popen, PIPE

import bones.event, logging
from bones.bot import Module, urlopener
from __main__ import *

class math(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		
	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="cc")
	def cmdCalc(self, event):
		prefix = "CALC"
		maxLen = 275
		constants = [
			"c=299792458",
			"pi=3.1415926535897932"
		]
		
		if event.args:
			try:
				calc = Popen("bc", stdin=PIPE, stdout=PIPE)
				calc_input = "".join(event.args).lower().replace(",", ".").encode('ascii')
				result = "".join(calc.communicate("%s;%s\n" % (";".join(constants), calc_input))[0].split('\\\n'))
				msg(event.channel.msg, prefix, "\x0314<\x03 %s" % calc_input)
				for line in result.split("\n"):
					if len(line.strip("\n")) >= 1:
						if len(line) < maxLen:
							if line.rstrip("\n").isdigit():
								msg(event.channel.msg, prefix, "\x0314=\x03 %s" % 
									"{0:,}".format(int(line)).replace(",", ",").strip("\n"))
							else:
								msg(event.channel.msg, prefix, "\x0314=\x03 " + line)
						else:
							warn(event.channel.msg, "Result too long for chat. Protip: Try http://wolframalpha.com")
			except OSError:
				logger.error("Could not fetch BC, is it installed?")
			except UnicodeDecodeError:
				error(event.channel.msg, "Input contains illegal characters.")
		else:
			warn(event.channel.msg, "You must provide a equation.")

	@bones.event.handler(trigger="bcon")
	@bones.event.handler(trigger="hex")
	@bones.event.handler(trigger="bin")
	@bones.event.handler(trigger="dec")
	def cmdBaseConverter(self, event):
		global out_dec, out_hex, out_bin, dec_input
		args = [arg.strip() for arg in " ".join(event.args).split(arg_separator)]
		if len(args) > 0:
			args[0] = re.sub('[^0-9a-zA-Z]+', ' ', args[0])
			event.args = [arg.strip() for arg in args[0].split(" ")]
			
		TriggerEvent = event.match.group(2).lower()
		out_dec, out_hex, out_bin, out_ascii, dec_input = [],[],[],[],[]
		hex_chars, dec_chars, bin_chars = (
			re.compile("[a-f*]", re.I),
			re.compile("[2-9*]", re.I),
			re.compile("[0-1*]", re.I),
		)

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
					if len(num.strip(" ")) > 0:
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
						msg(event.channel.msg, "Dec", dec_out)
					elif args[1].lower().startswith(("hex", "16")):
						msg(event.channel.msg, "Hex", hex_out)
					elif args[1].lower().startswith(("bin", "2")):
						msg(event.channel.msg, "Bin", bin_out)
					elif args[1].lower().startswith(("ascii", "txt")):
						msg(event.channel.msg, "TXT", "".join(out_ascii))
					else:
						warn(event.channel.msg, "Unknown output")
				else:
					msg(event.channel.msg, "Dec", dec_out)
					msg(event.channel.msg, "Hex", hex_out)
					msg(event.channel.msg, "Bin", bin_out)
			except ValueError:
				error(event.channel.msg, "Invalid number")
			except TypeError:
				error(event.channel.msg, "Invalid input")
		else:
			warn(event.channel.msg, "Usage: [Hex/Bin/Dec] Numbers to convert.")

class misc(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.ongoingPings = {}
		self.prefixChars = self.settings.get("bot", "triggerPrefixes")

	@bones.event.handler(trigger="pw")
	@bones.event.handler(trigger="password")
	def cmdPW(self, event):
		maxLen = 256
		tArgs = 16
		chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
		rand = "".join(random.choice(chars) for x in range(tArgs))
		if len(event.args) > 0:
			if int(event.args[0]) > int(maxLen):
				warn(event.channel.msg, "Length must be a valid number between 1 and 256!")
			else:
				tArgs = int(event.args[0])
				tArgs = max(1, min(tArgs, maxLen))
				rand = "".join(random.choice(chars) for x in range(tArgs))
				event.user.notice('Here you go: %s' % rand)
		else:
			event.user.notice('Here you go: %s' % rand)
			
	@bones.event.handler(trigger="tg")
	@bones.event.handler(trigger="tg15")
	def timetoTG14(self, event):
		tg15_start = (datetime.datetime(2015,4,1,9) - datetime.datetime.now())
		tg15_end = (datetime.datetime(2015,4,5,13) - datetime.datetime.now())
		if tg15_start.total_seconds() > 0:
			msg(event.channel.msg,
				"Det er \x0309%s\x03 dager, \x0309%s\x03 timer og \x0309%s\x03 minutter til \x0312The Gathering 2015\x03!" %
				(str(tg15_start.days), str(tg15_start.seconds//3600), str(tg15_start.seconds//60%60)))
		elif tg15_end.total_seconds() < 1:
			msg(event.channel.msg,
				"\x0312The Gathering 2015\x03 er over!")
		else:
			msg(event.channel.msg,
				"Det er \x0309%s\x03 dager, \x0309%s\x03 timer og \x0309%s\x03 minutter igjen av \x0312The Gathering 2015\x03!" %
				(str(tg15_end.days), str(tg15_end.seconds//3600), str(tg15_end.seconds//60%60)))

	"""
		TODO:
		* Add option to convert from spesific time/date
	"""
	@bones.event.handler(trigger="time")
	def timez(self, event):
		def autoCase(string):
			if "/" in string:
				stringList = string.lower().split("/")
				string = []
				for stringTmp in stringList:
					stringTmp = stringTmp.capitalize()
					if "_" in stringTmp:
						string_ = stringTmp.split("_")
						stringU = []
						for stringE in string_:
							stringU.append(stringE.capitalize())
						stringTmp = "_".join(stringU)
					string.append(stringTmp)
				if len(string[0]) == 2:
					string[0] = string[0].upper()
				string = "/".join(string)
			elif len(string) == 3:
				string = string.upper()
			return string

		time_fmt = "\x0309%H:%M:%S \x0312%d.%m.%Y %Z"
		if len(event.args) > 0 and pytz_available:
			try:
				tz = autoCase(event.args[0])
				if len(event.args) > 0:
					timehandle = datetime.datetime.now(pytz.timezone(tz))
				msg(event.channel.msg, "TIME", "The time for \"%s\":" % tz)
				msg(event.channel.msg, "TIME", timehandle.strftime(time_fmt))
			except pytz.exceptions.UnknownTimeZoneError:
				warn(event.channel.msg, "Unknown Timezone")
		else:
			msg(event.channel.msg, "The local time is: %s" % time.strftime(time_fmt))

	"""
		TODO:
		* Fetch subreddit-title/description
	"""
	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def stringResponses(self, event):
		msg_str = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if "r/" in event.msg.lower() and not event.msg.lower().startswith(self.prefixChars):
			if not "reddit.com" in event.msg.lower():
				try:
					subreddit =  "/r/" + re.match("[^.]*(\A|\s)+/?r/(\w+)", msg_str).group(2)
					subreddit_url = "https://reddit.com" + subreddit
					if len(subreddit) > 3:
						msg(event.channel.msg, "reddit \x0311::\x03 %s \x0311::\x03 %s" % 
							(subreddit, subreddit_url))
				except AttributeError:
					pass