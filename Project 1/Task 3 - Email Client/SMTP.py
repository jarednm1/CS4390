#!/usr/bin/python3

# python SMTP.py @gmail.com smtp.gmail.com
# pass
import sys
import argparse
import getpass
import certifi
import smtplib
import ssl
from email.mime.multipart import *
from email.mime.text import *
from email.mime.application import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email_id', type=str)
    parser.add_argument('attachment', type=str, nargs='?', default="")

    args = parser.parse_args()
    print(args.attachment)

    if args.email_id.partition("@")[2] == "gmail.com": # Set SMTP server for Google mail accounts
        mail_server = "smtp.gmail.com"
    else:
        mail_server = input('SMTP server:')

    if args.attachment != "":
        try:
            with open(args.attachment, "rb") as attachment:
                att = MIMEApplication(attachment.read(), _subtype='plain')
                att.add_header('Content-Disposition', "attachment; filename=%s" % args.attachment.split("/")[-1]) #Adding the correct header to the attachment with the filename
                print("sending mail with attachment")
                sendMail(args.email_id, mail_server, att)
                return 0
        except Exception as e:
            print(e)
            sendMail(args.email_id, mail_server)
            return 0
    else:
        sendMail(args.email_id, mail_server)
        return 0

def sendMail(email_id, email_server, attachment=None):
    pwd = getpass.getpass(prompt = 'type password for ' + email_id + '\n') #getpass method hides input
    receiver_id = input('receiver email address:')
    subject = input('subject of email:')
    print('getting message until eof:') #we'll support newlines and whatnot
    message = sys.stdin.read()
    #message = input('message text:')

    msg = MIMEMultipart('mixed') #Creating MIME object with proper tags
    msg['Subject'] = subject
    msg['From'] = email_id
    msg['To'] = receiver_id
    body = MIMEText(message, 'plain') #The message object is interpereted as plaintext
    msg.attach(body)

    if attachment != None:
        msg.attach(attachment)

    msg_full = msg.as_string() #Casting all data as a string for sendmail()

    port = 587
    with smtplib.SMTP(email_server, port) as server:
        try:
            print('communicating with your mail server...\n')
            context = ssl.create_default_context(cafile=certifi.where()) #certifi.where() locates the installed CA bundle in the certifi module
            server.starttls(context=context)
            server.ehlo() #Identifying ourselves to the SMTP server with a greeting. Hello, SMTP server.
            server.login(email_id, pwd)
            server.sendmail(email_id, receiver_id, msg_full) #msg object already contains all required metadata
        except Exception as err: #fail gracefully with debug info to stdout
            print(err)
    return 0

main()
