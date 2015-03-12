# encoding: utf-8
import platform
import time

import bones.event
from bones.bot import Module
from __main__ import *


class core(Module):

    @bones.event.handler(trigger="kdver")
    def return_ver(self, event):
        level = {
            "info": 1,
            "debug": 0,
        }
        msg(event.channel.msg, "INFO", "%s \x0309%s \x0312(%s)" %
            (module_name, module_version, module_date))
        if len(event.args) > 0:
            arg = event.args[0].lower()
            try:
                if level[arg] < 2:
                    msg(
                        event.channel.msg,
                        "INFO",
                        "System time:\x0309 %s" %
                        (time.strftime("%d.%m.%Y %H:%M:%S %Z"))
                    )
                if level[arg] < 1:
                    msg(
                        event.channel.msg,
                        "INFO",
                        "Running \x0309%s %s\x0F on \x0309%s" % (
                            platform.python_implementation(),
                            platform.python_version(),
                            platform.node())
                    )
                    msg(event.channel.msg, "INFO", "OS: \x0312%s %s" %
                        (platform.system(), platform.release()))
            except:
                return
