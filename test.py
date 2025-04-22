msg = {
	"-h --help": "Print this message",
	"-c --cli": "Enable CLI mode",
	"-d --dbpath <path>": "Set path to DB relative to CWD"
}
# Use list comprehension to create a new merged list
c = [k + v for k, v in msg.items()]

print(c)