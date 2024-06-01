#!/usr/bin/env python3

import sys, os, json, configparser, smtplib
from email.message import EmailMessage

BODY_DATA = sys.stdin.read()
print("Content-Type: text/plain; charset=utf-8")
if not BODY_DATA:
	print("Status: 400 Bad Request")
	print()
	print("Missing body")
	sys.exit(0)
if not "REMOTE_USER" in os.environ:
	print("Status: 400 Bad Request")
	print()
	print("Missing authenticated user")
	sys.exit(0)
print()


CONFIG = configparser.ConfigParser()
CONFIG.read("files/server.ini")
CONFIG = dict(CONFIG["SendMail"])

def startSmtp():
	smtpFactory = None
	if CONFIG["ssl"].lower() == "false":
		smtpFactory = smtplib.SMTP
	elif CONFIG["ssl"].lower() == "true":
		smtpFactory = smtplib.SMTP_SSL
	else:
		print("Invalid value for \"SSL\" in section [SendMail]")
		sys.exit(1)
	return smtpFactory(host=CONFIG["host"], port=CONFIG["port"], timeout=30)

def smtpLogin(smtp):
	if CONFIG["user"] and CONFIG["password"]:
		smtp.login(CONFIG["user"], CONFIG["password"])


msg = EmailMessage()
msg["Subject"] = "Restic user " + os.environ["REMOTE_USER"]
msg["From"] = CONFIG["sender"]
msg["To"] = CONFIG["recipient"]
msg.set_content(BODY_DATA)

with startSmtp() as smtp:
	smtpLogin(smtp)
	smtp.send_message(msg)

print("Mail sent")
