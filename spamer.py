from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import configparser
import sys

from threading import Thread

arrayEmails = []
threads = []

def mthreadLoginSend(email, msg, username, password):
	server = smtplib.SMTP(config.get("Settings", "Host") + ': ' + config.get("Settings", "Port"))
	server.starttls()
	server.login(username, password)
	server.sendmail(msg['From'], email, msg.as_string())
	print("Successfully sent email to %s:" % (email))
	server.quit()

try:
	config = configparser.ConfigParser()
	config.read("config.ini")

	with open("emails.txt") as file:
		arrayEmails = file.read().splitlines()

	msg = MIMEMultipart()

	# config settings
	username = config.get("Settings", "Username")
	password = config.get("Settings", "Password")
	msg['From'] = config.get("Settings", "EmailFrom")
	msg['Subject'] = config.get("Settings", "Subject")
	message = config.get("Settings", "Message")

	if ('.txt' in message or '.html' in message):
		with open(message) as file:
			message = file.read()

	msg.attach(MIMEText(message, config.get("Settings", "TypeMessage")))

except (KeyError, FileNotFoundError, smtplib.SMTPAuthenticationError) as e:
	print(e)
	sys.exit(0)
except smtplib.SMTPConnectError:
	print("SMTP Connect error!")
	sys.exit(0)

for email in arrayEmails:
	thread = Thread(target=mthreadLoginSend, args=(email, msg, username, password))
	thread.start()
	threads.append(thread)

for t in threads:
	t.join()