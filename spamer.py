from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import configparser
import sys

from threading import Thread

arrayEmails = []
threads = []

def mthreadSend(email):
	server.sendmail(msg['From'], email, msg.as_string())
	print("Successfully sent email to %s:" % (email))

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

	msg.attach(MIMEText(message, 'plain'))

	server = smtplib.SMTP(config.get("Settings", "Host") + ': ' + config.get("Settings", "Port"))
	server.starttls()
	server.login(username, password)

except (KeyError, FileNotFoundError, smtplib.SMTPAuthenticationError) as e:
	print(e)
	sys.exit(0)
except smtplib.SMTPConnectError:
	print("SMTP Connect error!")
	sys.exit(0)

for email in arrayEmails:
	thread = Thread(target=mthreadSend, args=(email,))
	thread.start()
	threads.append(thread)

for t in threads:
	t.join()

server.quit()