# encoding: utf-8
from subprocess import Popen, PIPE
import datetime
import string
import random
import time
import re

try:
    import pytz
    pytz_available = True
except ImportError:
    pytz_available = False

from bones.bot import Module
from __main__ import *
import bones.event


class math(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)

    @bones.event.handler(trigger="calc")
    @bones.event.handler(trigger="cc")
    @bones.event.handler(trigger="bc")
    def cmdCalc(self, event):
        """Calculator (Bench Calculator)"""
        maxLen = 275    # Maximum output length
        constants = [   # Pre-defined variables
            "c=299792458",
            "pi=3.1415926535897932",
            "scale=5"
        ]
        if event.args:
            try:
                calc = Popen("bc", stdin=PIPE, stdout=PIPE)
                calc_input = (
                    " ".join(event.args).lower()
                    .replace(",", ".").encode('ascii'))
                result = "".join(calc.communicate("%s;%s\n" % (
                    ";".join(constants), calc_input))[0].split('\\\n'))
                msg(event.channel.msg, "CALC", "\x0314<\x0F %s" % calc_input)

                for line in result.split("\n"):
                    if len(line.strip("\n")) >= 1:
                        if len(line) < maxLen:
                            if line.rstrip("\n").isdigit():
                                msg(
                                    event.channel.msg, "CALC",
                                    "\x0314=\x0F %s" %
                                    "{0:,}".format(int(line))
                                    .replace(",", ",").strip("\n"))
                            else:
                                msg(
                                    event.channel.msg, "CALC",
                                    "\x0314=\x0F " + line)
                        else:
                            warn(
                                event.channel.msg,
                                "Result too long for chat. Try http://wolframalpha.com")
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
        """Base Converter
        Create a list containing a string of all
        input values and the optional output format
        """
        args = [
            arg.strip() for arg in " ".join(event.args).split(ARG_SEPARATOR)
        ]
        if len(args) > 0:
            args[0] = re.sub('[^0-9a-zA-Z]+', ' ', args[0])
            event.args = [arg.strip() for arg in args[0].split(" ")]

        TriggerEvent = event.match.group(2).lower()
        out_dec, out_hex, out_bin, out_ascii, dec_input = (
            [], [], [], [], []
        )
        # Compile regex objects for valid characters of each base
        hex_chars, dec_chars, bin_chars = (
            re.compile("[a-f*]", re.I),
            re.compile("[2-9*]", re.I),
            re.compile("[0-1*]", re.I),
        )

        # Select input base based on the trigger used
        if len(event.args) >= 1:
            if TriggerEvent == "hex":
                sourcebase = "16"
            elif TriggerEvent == "bin":
                sourcebase = "2"
            elif TriggerEvent == "dec":
                sourcebase = "10"
            # If the first step fails look at the first input argument
            else:
                if event.args[0].lower().startswith(("0x", "hex")):
                    sourcebase = "16"
                    # Delete the first argument if is a match
                    if event.args[0].lower() == "hex":
                        del event.args[0]
                elif event.args[0].lower().startswith(("0b", "bin")):
                    sourcebase = "2"
                    if event.args[0].lower() == "bin":
                        del event.args[0]
                elif event.args[0].lower() == "dec":
                    sourcebase = "10"
                    del event.args[0]

                # And if the second step fails try to detect the base automatically
                elif hex_chars.search("".join(event.args)):
                    sourcebase = "16"
                elif dec_chars.search("".join(event.args)):
                    sourcebase = "10"
                elif bin_chars.search("".join(event.args)):
                    sourcebase = "2"

            try:
                # Convert input values to decimal and separate them in a list
                for num in event.args:
                    if len(num.strip(" ")) > 0:
                        dec_input.append(int(num, int(sourcebase)))
                # Convert and place the items into lists with their hex and bin corresponding values
                for num in dec_input:
                    out_dec.append(str(num))
                    out_hex.append(hex(num))
                    out_bin.append(bin(num))
                    # If the output arg is set to "ascii" or "txt" convert them into a string
                    if len(args) > 1:
                        if args[1].lower().startswith(("ascii", "txt")):
                            out_ascii.append(
                                hex(num).replace("0x", "").decode("hex"))

                # Separate the values using spaces
                dec_out = " ".join(out_dec)
                hex_out = " ".join(out_hex).replace("0x", "").upper()
                # Limit binary output to 128 characters
                if len("".join(out_bin)) > 128:
                    decrease = len("".join(out_bin)) - 128
                    bin_out = (
                        " ".join(out_bin).replace("0b", "").replace('', '')
                        [:-decrease].upper() + "...")
                else:
                    bin_out = " ".join(out_bin).replace("0b", "")

                # Print specified output value
                if len(args) > 1:
                    if args[1].lower().startswith(("dec", "10")):
                        msg(event.channel.msg, "DEC", dec_out)
                    elif args[1].lower().startswith(("hex", "16")):
                        msg(event.channel.msg, "HEX", hex_out)
                    elif args[1].lower().startswith(("bin", "2")):
                        msg(event.channel.msg, "BIN", bin_out)
                    elif args[1].lower().startswith(("ascii", "txt")):
                        msg(event.channel.msg, "TXT", "".join(out_ascii))
                    else:
                        warn(event.channel.msg, "Unknown output")
                # If none specified print dec, hec and binary
                else:
                    msg(event.channel.msg, "DEC", dec_out)
                    msg(event.channel.msg, "HEX", hex_out)
                    msg(event.channel.msg, "BIN", bin_out)
            except ValueError:
                error(event.channel.msg, "Invalid number")
            except TypeError:
                error(event.channel.msg, "Invalid input")
        else:
            warn(event.channel.msg, "Usage: [Hex/Bin/Dec] Numbers to convert.")


class misc(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.TIME_FMT = "\x0309%H.%M.%S \x0312%d.%m.%Y %Z"

    @bones.event.handler(trigger="pw")
    @bones.event.handler(trigger="password")
    def cmdPW(self, event):
        """Password Generator"""
        maxLen = 256  # Maximum allowed password length
        tArgs = 16    # Default password length
        chars = (     # Characters to be used in the password
            string.ascii_uppercase +
            string.ascii_lowercase +
            string.digits
        )
        rand = "".join(random.choice(chars) for x in range(tArgs))
        if len(event.args) > 0:
            if int(event.args[0]) > int(maxLen):
                warn(
                    event.channel.msg,
                    "Length must be a valid number between 1 and 256!")
            else:
                tArgs = int(event.args[0])
                tArgs = max(1, min(tArgs, maxLen))
                rand = "".join(random.choice(chars) for x in range(tArgs))
                event.user.notice('Here you go: %s' % rand)
        else:
            event.user.notice('Here you go: %s' % rand)

    @bones.event.handler(trigger="tg")
    @bones.event.handler(trigger="tg18")
    @bones.event.handler(trigger="tg17")
    @bones.event.handler(trigger="tg16")
    @bones.event.handler(trigger="2018")
    @bones.event.handler(trigger="2017")
    @bones.event.handler(trigger="2016")
    @bones.event.handler(trigger="2038")
    @bones.event.handler(trigger="countdown")
    def countdown(self, event):
        """Countdown timer
        Events must be specified in the events dictionary bellow
        with the event-id containing some attributes
        Valid attributes are:
        "titlestr" (Required) the title of the event
        "start" (Required) a naive datetime object containing the start date
        "end" (required) same as above but with the end date/time
        "aliases" (optional) a list of triggers that can be used
        *All dates must be specified in UTC
        """
        events = {
            "2018": {
                "titlestr": "\x03092018",
                "start": datetime.datetime(2017, 12, 31, 23),
                "end": datetime.datetime(2018, 12, 31, 23)
            },

            "2017": {
                "titlestr": "\x03092017",
                "start": datetime.datetime(2016, 12, 31, 23),
                "end": datetime.datetime(2017, 12, 31, 23)
            },

            "2016": {
                "titlestr": "\x03092016",
                "start": datetime.datetime(2015, 12, 31, 23),
                "end": datetime.datetime(2016, 12, 31, 23)
            },

            "tg18": {
                "titlestr": "\x0306The Gathering 2018",
                "start": datetime.datetime(2018, 3, 28, 7),
                "end": datetime.datetime(2017, 4, 1, 10),
                "aliases": [
                    "tg",
                    "gathering",
                    "The Gathering 2018",
                    "Gathering 2018"
                ]
            },

            "tg17": {
                "titlestr": "\x0306The Gathering 2017",
                "start": datetime.datetime(2017, 4, 12, 7),
                "end": datetime.datetime(2017, 4, 16, 10),
                "aliases": [
                    "The Gathering 2017",
                    "Gathering 2017"
                ]
            },

            "tg16": {
                "titlestr": "\x0304The Gathering 2016",
                "start": datetime.datetime(2016, 3, 23, 8),
                "end": datetime.datetime(2016, 3, 27, 10),
                "aliases": [
                    "The Gathering 2016",
                    "Gathering 2016"
                ]
            },

            "2038": {
                "titlestr": "\x0311The Year 2038 Bug",
                "start": datetime.datetime(2038, 1, 19, 3, 14, 7),
                "end": datetime.datetime(2038, 1, 19, 3, 14, 7),
                "aliases": [
                    "year2038"
                ]
            },
        }

        def countdownStrValues(timeremaining, timevalues=[]):
            """Return a generated string with the
            days, hours and minutes left until timeremaining.
            """
            minleft = True if timeremaining.total_seconds() <= 60 else False
            if timeremaining.days > 0:
                timevalues.append(
                    "\x0309%s\x0F dager" %
                    str(timeremaining.days))
            if timeremaining.seconds//3600 > 0:
                timevalues.append(
                    "\x0309%s\x0F timer" %
                    str(timeremaining.seconds // 3600))
            if timeremaining.seconds // 60 % 60 > 0 or minleft:
                timevalues.append(
                    "\x0309%s\x0F minutter" %
                    str(timeremaining.seconds // 60 % 60))
            if len(timevalues) > 1:
                timevalues.reverse()
                timevalues.insert(1, "og")
                if len(timevalues) > 2:
                    n = 3
                    while n < len(timevalues):
                        timevalues.insert(n, timevalues.pop(n) + ",")
                        n = n + 1
                timevalues.reverse()
            return(" ".join(timevalues))

        #def countdownStrValuesMin(targetevent, timevalues=[]):
        #

        try:
            cEvent = None
            triggerEvent = event.match.group(2).lower()
            # Search for the input arg/trigger in event dict and it's aliases.
            for i, k in events.iteritems():
                # Create aliases list if event doesn't have one
                i, k1 = i.lower(), []
                if "aliases" in k:
                    for k2 in k["aliases"]: k1.append(k2.lower())
                aliases = k1 + [i] if "aliases" in k else [i]
                # Search with input arg, ignore if previous round succeeded
                if len(event.args) > 0 and cEvent is None:
                    arg = " ".join(event.args).lower()
                    if arg in aliases:
                        cEvent = events[i]
                # Same as above but with the input trigger
                if triggerEvent in aliases:
                    cEvent = events[i]

            # Raise a KeyError exception if no event could be found
            if cEvent is None and len(event.args) > 0:
                raise KeyError

            if cEvent:
                # Calculate the remaining time to the event start/end
                remainingtime = {
                    "start": cEvent["start"] - datetime.datetime.utcnow(),
                    "end": cEvent["end"] - datetime.datetime.utcnow()
                }
                if remainingtime["start"].total_seconds() > 0:
                    msg(
                        event.channel.msg, "Det er %s til %s\x0F!" % (
                            countdownStrValues(remainingtime["start"]),
                            cEvent["titlestr"]))
                elif remainingtime["end"].total_seconds() < 1:
                    msg(
                        event.channel.msg, "%s\x0F er over!" %
                        cEvent["titlestr"])
                else:
                    msg(
                        event.channel.msg, "Det er %s igjen av %s\x0F!" % (
                            countdownStrValues(remainingtime["end"]),
                            cEvent["titlestr"]))
            else:
                msg(
                    event.channel.msg,
                    "Countdown",
                    "Usage: !countdown [Event]"
                )

        except KeyError:
            warn(event.channel.msg, "Unknown Event")

    @bones.event.handler(trigger="time")
    def timeTool(self, event):
        """World clock"""
        def autoCase(string):
            """Capitalizes Region/City format inputs
            and makes all letters in 2/3 letter Country-Codes upper-case
            """
            if "/" in string:
                stringList = string.lower().split("/")
                string = []
                for stringTmp in stringList:
                    stringTmp = stringTmp.capitalize()
                    if "_" or "-" in stringTmp:
                        if "-" in stringTmp:
                            dash = "-"
                        else:
                            dash = "_"
                        string_ = stringTmp.split(dash)
                        stringU = []
                        for stringE in string_:
                            stringU.append(stringE.capitalize())
                        stringTmp = dash.join(stringU)
                    string.append(stringTmp)
                if len(string[0]) == 2:
                    string[0] = string[0].upper()
                string = "/".join(string)
            else:
                string = string.upper()
            return string

        # Print UNIX-Timestamp if input arg is "unix"
        if len(event.args) > 0 and event.args[0].lower() == "unix":
            msg(
                event.channel.msg, "TIME",
                "UNIX-timestamp: \x0309%s" % int(time.time())
            )
        # Print time in specified time-zone if pytz is available
        elif len(event.args) > 0 and pytz_available:
            try:
                if len(event.args[0]) == 2:
                    tz = str(pytz.country_timezones[event.args[0].lower()][0])
                else:
                    tz = autoCase(event.args[0])
                if len(event.args) > 0:
                    timehandle = datetime.datetime.now(pytz.timezone(tz))
                msg(
                    event.channel.msg, "TIME",
                    "The time in \"%s\":" % tz)
                msg(
                    event.channel.msg, "TIME",
                    timehandle.strftime(self.TIME_FMT)
                )
            except pytz.exceptions.UnknownTimeZoneError:
                warn(event.channel.msg, "Unknown Timezone")
            except KeyError:
                warn(
                    event.channel.msg,
                    "Unknown Country-Code. See https://www.iso.org/obp/ui/#search/code/"
                )
        # Print local-time if pytz is not available
        else:
            msg(
                event.channel.msg,
                "The local time is: %s" % time.strftime(self.TIME_FMT)
            )


class mctools(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)

    @bones.event.handler(trigger="mcolor")
    def mcColorCode(self, event):
        """Minecraft Color Code Generator"""
        ValueisLegal = True
        if len(event.args) > 0:
            if "," in "".join(event.args):
                event.args = "".join(event.args).split(ARG_SEPARATOR)
            if len(event.args) == 1:
                event.args.insert(0, "0")
            if len(event.args) == 2:
                event.args.insert(0, "0")
            for i in event.args:
                if i.isdigit() == 0 or int(i) > 255:
                    ValueisLegal = False
        else:
            event.args = None
        if event.args is not None and ValueisLegal:
            r, g, b = (
                int(event.args[0]),
                int(event.args[1]),
                int(event.args[2]))
            formula = (r << 16) + (g << 8) + b
            msg(event.channel.msg, "MC-Color", "\x0314=\x0F " + str(formula))
        elif event.args is None:
            warn(event.channel.msg, "Specify a valid RGB Value.")
        else:
            error(event.channel.msg, "Input must be a valid RGB value.")


class responses(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.prefixChars = self.settings.get("bot", "triggerPrefixes")

    @bones.event.handler(event=bones.event.ChannelMessageEvent)
    def stringResponses(self, event):
        """Automatic String Responses"""
        msg_str = re.sub(
            "\x02|\x1f|\x1d|\x16|\x0f|\x03\d{0,2}(,\d{0,2})?",
            "", event.message
        )
        # Reddit
        if "r/" in event.message.lower():
            if not event.message.lower().startswith(self.prefixChars):
                if "reddit.com" not in event.message.lower():
                    try:
                        subreddit = (
                            "/r/" + re.match(
                                "[^.]*(\A|\s)+/?r/(\w+)",
                                msg_str).group(2))
                        subreddit_url = "https://reddit.com" + subreddit
                        if len(subreddit) > 3:
                            msg(
                                event.channel.msg,
                                "reddit \x0311::\x0F %s \x0311::\x0F %s" %
                                (subreddit, subreddit_url))

                    except AttributeError:
                        pass
