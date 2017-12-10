import smtpd
import asyncore
import pythonwhois
import tldextract
import smtplib
import traceback
import datetime

MAX_DAYS = 15
FILTER_HOST = '127.0.0.1'
FILTER_PORT = 10025
POSTFIX_HOST = '127.0.0.1'
POSTFIX_PORT = 10026

class CustomSMTPServer(smtpd.SMTPServer):

	def process_message(self, peer, mailfrom, rcpttos, data):
		
		mailfrom.replace('\'', '')
		mailfrom.replace('\"', '')
		
		for recipient in rcpttos:
			recipient.replace('\'', '')
			recipient.replace('\"', '')
		
#		print('Receiving message from:', peer)
#		print('Message addressed from:', mailfrom)
#		print('Message addressed to  :', rcpttos)
#		print('MSG >>')
#		print(data)
#		print('>> EOT')

		try:
			extracted = tldextract.extract(mailfrom)
			domain_info = pythonwhois.get_whois("%s.%s" % (extracted.domain, extracted.suffix))
			delta = datetime.datetime.now() - domain_info.get('creation_date', [datetime.datetime.now()])[0]
			print('Sender\'s domain %s created %d days ago' % (mailfrom, delta.days))
			if delta.days < MAX_DAYS:
				print('Prevent delivery from suspicious sender: %s' % (maifrom))
				return
		except:
			pass
			print('Something went south')
			print(traceback.format_exc())

		try:
			server = smtplib.SMTP(POSTFIX_HOST, POSTFIX_PORT)
			server.sendmail(mailfrom, rcpttos, data)
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
