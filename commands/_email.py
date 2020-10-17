# Tutorial Used: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

verificationCodes = {}


def send_email(receiver_address, mail_body, subject):
    sender_address = os.getenv("GMAIL_USER")
    sender_password = os.getenv("GMAIL_PASS")

    receiver_address = receiver_address
    # Setup the Multipurpose Internet Mail Connection

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.attach(MIMEText(mail_body))

    gmail_smtp_port = 587
    session = smtplib.SMTP('smtp.gmail.com', gmail_smtp_port)
    session.starttls()  # enable security
    session.login(sender_address, sender_password)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def send_confirmation_email(receiver_address, user_id):
    unique_key = get_unique_key()

    mail_body = '''Please verify your email address by typing $confirm {0} in the #verification channel of the Tron 2025 Discord server! '''

    verificationCodes[user_id] = unique_key

    send_email(receiver_address, mail_body.format(unique_key), 'Tron 2025 Discord Server Confirmation')


def get_unique_key():
    length = 10
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
