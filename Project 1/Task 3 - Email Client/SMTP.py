#!/usr/bin/python3

import argparse
import getpass
import certifi
import smtplib
import ssl
from email.mime.text import MIMEText

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email_id', type=str)
    parser.add_argument('mail_server', type=str)
    args = parser.parse_args()
    sendMail(args.email_id, args.mail_server)
    return 0

def sendMail(email_id, email_server):
    pwd = getpass.getpass(prompt = 'type password for ' + email_id + '\n')
    receiver_id = input('receiver email address:')
    subject = input('subject of email:')
    message = input('message text:')

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email_id
    msg['To'] = receiver_id

    port = 587
    with smtplib.SMTP(email_server, port) as server:
        try:
            print('communicating with your mail server...\n')
            context = ssl.create_default_context(cafile=certifi.where())
            server.starttls(context=context)
            server.ehlo()
            server.login(email_id, pwd)
            server.send_message(msg)
        except Exception as err:
            print(err)
    return 0

main()
