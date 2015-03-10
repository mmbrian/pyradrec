#!/usr/bin/env /usr/local/bin/python2.7

import re
import smtplib
from email.mime.text import MIMEText
import settings

class SMTPConnection:

    mail_server = None

    def __init__(self, show_communication = True):
        # print 'connecting to %s...' % settings.EMAIL_HOST
        try:

            self.mail_server = smtplib.SMTP()
            self.mail_server.connect(settings.EMAIL_HOST)
            self.mail_server.set_debuglevel(show_communication)
            
            self.mail_server.ehlo()
            self.mail_server.starttls()
            self.mail_server.ehlo()
            self.mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        except Exception as err:
            print "Error: ", err
            return
        # print "successfully initialized SMTP connection with %s..." % settings.EMAIL_HOST

    @staticmethod
    def create_message(subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        return msg

    def send_mail(self, message, author, recipients):
        try:
            self.mail_server.sendmail(author,
                                      recipients,
                                      message.as_string())
        except Exception as err:
            print "Error: ", err
        finally:
            self.mail_server.close()


def send_mail(subject, body = ""):
    author = settings.EMAIL_RECIPIENT
    recipients = [settings.EMAIL_RECIPIENT]
    
    subject = "Radio Recording Session: " + subject

    try:
        message = SMTPConnection.create_message(subject, body)
    except Exception as err:
        print 'Error: ', err
        return
    # print 'successfully created email message...\nready to send mail...'
	
    con = SMTPConnection(False)
    try:
        con.send_mail(message, author, recipients)
	# print 'message successfully sent.'
	return True
    except Exception as err:
        print 'Error: ', err
        return False
    


