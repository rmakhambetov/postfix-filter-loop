import smtpd
import asyncore
import pythonwhois
import tldextract
import smtplib
import traceback
import datetime
import argparse
import sys

parser=argparse.ArgumentParser()

parser.add_argument('--postfix-host', help='Specify address where postfix is hosted')
parser.add_argument('--postfix-port', help='Specify port where postfix is hosted')
parser.add_argument('--filter-host', help='Specify address where filter-server is hosted')
parser.add_argument('--filter-port', help='Specify port where filter-server is hosted')
parser.add_argument('--max-days', help='Specify days')
args=parser.parse_args()

MAX_DAYS = int(args.max_days)
POSTFIX_HOST = args.postfix_host or 'localhost'
POSTFIX_PORT = int(args.postfix_port)
FILTER_HOST = args.filter_host or 'localhost'
FILTER_PORT = int(args.filter_port)

class CustomSMTPServer(smtpd.SMTPServer):

	def process_message(self, peer, mailfrom, rcpttos, data):
		
		mailfrom.replace('\'', '')
		mailfrom.replace('\"', '')

		try:
			extracted = tldextract.extract(mailfrom)
			domain_info = pythonwhois.get_whois("%s.%s" % (extracted.domain, extracted.suffix))
			delta = datetime.datetime.now() - domain_info.get('creation_date', [datetime.datetime.now()])[0]
			print('Sender\'s domain %s created %d days ago' % (mailfrom, delta.days))
			if delta.days < MAX_DAYS:
				print('Prevent delivery from suspicious sender: %s' % (mailfrom))
				return
		except:
			pass
			print('Something went south')
			print(traceback.format_exc())

		try:
			server = smtplib.SMTP(POSTFIX_HOST, POSTFIX_PORT)
			print(server.sendmail(mailfrom, rcpttos, data))
			server.quit()
#			print('send successful')
		except smtplib.SMTPException:
			print('Exception SMTPException')
			pass
		except smtplib.SMTPServerDisconnected:
			print('Exception SMTPServerDisconnected')
			pass
		except smtplib.SMTPResponseException:
			print('Exception SMTPResponseException')
			pass		
		except smtplib.SMTPSenderRefused:
			print('Exception SMTPSenderRefused')
			pass		
		except smtplib.SMTPRecipientsRefused:
			print('Exception SMTPRecipientsRefused')
			pass		
		except smtplib.SMTPDataError:
			print('Exception SMTPDataError')
			pass		
		except smtplib.SMTPConnectError:
			print('Exception SMTPConnectError')
			pass		
		except smtplib.SMTPHeloError:
			print('Exception SMTPHeloError')
			pass		
		except smtplib.SMTPAuthenticationError:
			print('Exception SMTPAuthenticationError')
			pass
		except:
			print('Undefined exception')
			print(traceback.format_exc())

		return
		
server = CustomSMTPServer((FILTER_HOST, FILTER_PORT), None)

asyncore.loop()
