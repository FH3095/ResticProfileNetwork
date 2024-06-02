#!/usr/bin/env python3

import sys
import funcs

#sys.argv = ["sendLog.py", "log.txt", "MailSubject"]
CONFIG = funcs.Config()

if len(sys.argv) < 2:
    print("Missing arguments to send logs", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1], mode="rt") as file:
    funcs.sendMail(CONFIG.url + "/sendMail.py", (CONFIG.username, CONFIG.password), CONFIG.ssl, sys.argv[2], file.read())
