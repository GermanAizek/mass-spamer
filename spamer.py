from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import configparser
import sys

from threading import Thread
from time import sleep

arrayEmails = []
threads = []

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def mthreadLoginSend(email, msg, username, password):
	server = smtplib.SMTP(config.get("Settings", "Host") + ': ' + config.get("Settings", "Port"))
	server.starttls()
	server.login(username, password)
	server.sendmail(msg['From'], email, msg.as_string())
	print("Successfully sent email to %s:" % (email))
	server.quit()
	sleep(1)

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

length = len(threads)
printProgressBar(0, length, prefix = 'Sending:', suffix = 'Complete', length = 50)
for idx, t in enumerate(threads):
	t.join()
	sleep(1)
	printProgressBar(idx + 1, length, prefix = 'Sending:', suffix = 'Complete', length = 50)