from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

msg = MIMEMultipart()

message = "Mass spam"

password = "your_password"
user = "your_username"
msg['From'] = "name@mail.com"
msg['To'] = "client@mail.com"
msg['Subject'] = "Test subscription"

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('mail.host.com: host_port')
server.starttls()
server.login(user, password)

server.sendmail(msg['From'], msg['To'], msg.as_string())

server.quit()

print("successfully sent email to %s:" % (msg['To']))