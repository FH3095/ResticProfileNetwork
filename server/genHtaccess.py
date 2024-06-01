#!/usr/bin/env python3

import os, json, base64, hashlib

ENCODING = "ascii"
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

FILES_HTACCESS = """
Require all denied

AuthType Basic
AuthName "get"
AuthBasicProvider file
AuthUserFile "{ScriptPath}/files/.htpasswd"
"""

PUBLIC_HTACCESS = """
Require valid-user
"""

PRIVATE_HTACCESS = """
Require all denied

{FilesSections}
"""

PRIVATE_FILES_SECTION = """
<Files "conf-{UserName}.*">
	Require user {UserName}
</Files>
"""

SEND_MAIL_HTACCESS = """
<Files "sendMail.py">
	AuthType Basic
	AuthName "get"
	AuthBasicProvider file
	AuthUserFile "{ScriptPath}/files/.htpasswd"

	Options +ExecCGI
	SetHandler cgi-script
</Files>
"""

# Create private and public sub-directories
os.makedirs("files/public", exist_ok=True)
os.makedirs("files/private", exist_ok=True)

# Write sendMail htaccess
with open(".htaccess", mode="wt", encoding=ENCODING) as file:
    file.write(SEND_MAIL_HTACCESS.format(ScriptPath=SCRIPT_PATH))

# Read users and write files/.htpasswd
users = None
with open("files/users.json", mode="rt", encoding=ENCODING) as file:
	users = json.load(file)
with open("files/.htpasswd", mode="wt", encoding=ENCODING) as file:
	for username, password in users.items():
		hash = hashlib.sha1(password.encode(ENCODING))
		hash = base64.standard_b64encode(hash.digest()).decode(ENCODING)
		print(username, ":{SHA}", hash, sep="", file=file)

# Write generic files/.htaccess
with open("files/.htaccess", mode="wt", encoding=ENCODING) as file:
	file.write(FILES_HTACCESS.format(ScriptPath=SCRIPT_PATH))

# Write .htaccess for public
with open("files/public/.htaccess", mode="wt", encoding=ENCODING) as file:
	file.write(PUBLIC_HTACCESS)

# Write .htaccess for private
filesSections = ""
for username in users.keys():
	filesSections += PRIVATE_FILES_SECTION.format(UserName=username)
with open("files/private/.htaccess", mode="wt", encoding=ENCODING) as file:
	file.write(PRIVATE_HTACCESS.format(FilesSections=filesSections))
