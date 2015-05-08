# encoding: utf-8
import platform
import time

import bones.event
from bones.bot import Module
from __main__ import *


class core(Module):

    @bones.event.handler(trigger="kdver")
    def return_ver(self, event):
        LEVEL = {
            "info": 1,
            "debug": 0,
        }
        msg(event.channel.msg, "INFO", "%s \x0309%s \x0312(%s)" %
            (MODULE_NAME, MODULE_VERSION, MODULE_DATE))
        if len(event.args) > 0:
            arg = event.args[0].lower()
            try:
                if LEVEL[arg] < 2:
                    msg(event.channel.msg, "INFO",
                        "System time:\x0309 %s" %
                        (time.strftime("%d.%m.%Y %H:%M:%S %Z"))
                    )
                if LEVEL[arg] < 1:
                    msg(event.channel.msg, "INFO",
                        "Running \x0309%s %s\x0F on \x0309%s" % (
                            platform.python_implementation(),
                            platform.python_version(),
                            platform.node())
                    )
                    msg(event.channel.msg, "INFO", "OS: \x0312%s %s" %
                        (platform.system(), platform.release()))
            except:
                return
