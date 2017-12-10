import sys
import smtpd
import asyncore

import smtplib
from email.mime.text import MIMEText
server = smtplib.SMTP('localhost', 10025)

me = 'rmakhambetov@lol1231113.io'
you = 'root@vsrv'
msg = MIMEText('Test msg to test before queue filter')

msg['Subject'] = 'Test message to test before filter'
msg['From'] = me
msg['To'] = you
server.sendmail(me, [you], msg.as_string())
server.quit()