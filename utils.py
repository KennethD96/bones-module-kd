# encoding: utf-8
import os
import string, random, re
import time, datetime
import urllib
from subprocess import Popen, PIPE

import bones.event, logging
from bones.bot import Module, urlopener
from __main__ import *

class math(Module):
	def __init__(self, *args, **kwargs):
		Module.__init__(self, *args, **kwargs)
		self.ccon_last_update = datetime.datetime(1970,1,1)
		
	@bones.event.handler(trigger="calc")
	@bones.event.handler(trigger="cc")
	def cmdCalc(self, event):
		prefix = "CALC"
		maxLen = 275
		constants = {
			"c":"299792458",
			"k":"000",
			"pi":"3.1415926535897932"
		}
		if not event.args:
			msg(event.channel.msg, "Please provide a equation")
		else:
			try:
				calc = Popen("bc", stdin=PIPE, stdout=PIPE)
				calc_input = "".join(event.args).lower().replace(",", ".")
				for wrd, value in constants.iteritems():
					if wrd in calc_input:
						calc_input = calc_input.replace(wrd, value)
				
				result = "".join(calc.communicate("%s\n" % calc_input)[0].split('\\\n')).split("\n")
				msg(event.channel.msg, prefix, "\x0314<\x03 %s" % (calc_input))
				for line in result:
					if len(line.strip("\n")) >= 1:
						if len(line) > maxLen:
							warn(event.channel.msg, "Result too long for chat. Protip: Try http://wolframalpha.com")
						else:
							if line.rstrip("\n").isdigit():
								msg(event.channel.msg, prefix, "\x0314=\x03 %s" % 
									"{0:,}".format(int(line)).replace(",", ",").strip("\n")
								)
							else:
								msg(event.channel.msg, prefix, "\x0314=\x03 " + line)
			except OSError:
				logger.error("Could not fetch BC, is it installed?")
		
	#@bones.event.handler(trigger="ccon")
	#def CurrencyConvert(self, event):
	#	api_url = "https://www.dnb.no/portalfront/datafiles/miscellaneous/csv/kursliste_ws.xml"
	#	cachepath = os.path.join(cache_path, "currency_db.xml.cache")
	#	db_update = datetime.datetime(today.year, today.month, today.day, 9)
	#	
	#	if self.ccon_last_update < db_update and datetime.datetime.now() > db_update:
	#		if not os.path.exists(cachepath):
	#			os.makedirs(cachepath)
	#		try:
	#			data = urlopener.open(api_url).read()
	#			with open(cachepath, "w") as cachefile:
	#				cachefile.write(data)
	#		except:
	#			data = open(cachepath, "r").read()
	#			logger.warn("Could not download currency database")
	#		logger.info("Currency database successfully updated!")
	#		self.ccon_last_update = datetime.datetime.now()
	#	else:
	#		data = open(cachepath, "r").read()

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
	@bones.event.handler(trigger="tg14")
	def timetoTG14(self, event):
		tg14_timeleft = (datetime.datetime(2014,04,16,9) - datetime.datetime.now())
		msg(event.channel.msg,
			"Det er\x039 %s\x03 dager og\x039 %s\x03 timer til \x0312TG14\x03!" %
			(str(tg14_timeleft.days), str(tg14_timeleft.seconds//3600)))

	@bones.event.handler(trigger="time")
	def localtime(self, event):
		msg(event.channel.msg, "The time is: %s" % time.strftime("\x0312%d.%m.%Y \x0309%H:%M:%S"))

	@bones.event.handler(trigger="parsev6")
	def ipv6parser(self, event):
		addr = event.args[0].strip("[]").lower()
		if re.findall("[^0-9a-f:]+", addr):
			error(event.channel.msg, "Address can only contain hex characters")
			return
		else:
			addr = addr.replace("::", ":x:").split(":")
			output = []
		try:
			addr.remove("")
		except:
			pass
		
		if addr.count("x") == 1:
			xpos = addr.index("x")
			addr.remove("x")
			while len(addr) < 8:
				addr.insert(xpos, "0000")
		elif addr.count("x") > 1:
			error(event.channel.msg, "Zero's can only be omitted once")
			return
		for item in addr:
			if len(item) > 4:
				error(event.channel.msg, "Each section cannot contain more than 4 numbers")
				return
			while len(item) < 4:
				item = "0" + item
			output.append(item)

		if len(addr) < 8:
			error(event.channel.msg, "Incomplete address")
			return
		elif len(addr) > 8:
			error(event.channel.msg, "Invalid address")
			return
		msg(event.channel.msg, "IPv6", ":".join(output))

	@bones.event.handler(event=bones.event.PrivmsgEvent)
	def stringResponses(self, event):
		msg_str = re.sub("\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?", "", event.msg)
		if "r/" in event.msg.lower():
			if not "reddit.com" in event.msg.lower():
				try:
					redditurl = "http://reddit.com"
					subreddit =  "/r/" + re.match("(\A|\s|/)r/(\w+)", msg_str).group(2)
					if len(subreddit) > 3:
						msg(event.channel.msg, "reddit \x0311::\x03 %s \x0311::\x03 %s" % 
							(subreddit, redditurl + subreddit))
				except:
					return
			
	@bones.event.handler(trigger="ping")
	def cmdPing(self, event):
		nick = event.user.nickname
		if nick not in self.ongoingPings:
			self.ongoingPings[nick] = event.channel.name
			event.user.ping()
		else:
			event.user.notice("Please wait until your ongoing ping in %s is finished until trying again." %
			self.ongoingPings[nick])
			
	@bones.event.handler(event=bones.event.CTCPPongEvent)
	def eventPingResponseReceive(self, event):
		nick = event.user.nickname
		if nick in self.ongoingPings:
			event.user.notice("%s: Your response time was %.3f seconds." % (nick, event.secs))
			del self.ongoingPings[nick]
