#Tutorial Used: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(receiverAddress, mail_body, subject):
    sender_address = 'bedibot2025@gmail.com'
    sender_password = 'd4w7!GG8TPvA'

    receiver_address = receiverAddress
    #Setup the Miltipurpose Internet Mail Conection

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.attach(MIMEText(mail_body, 'plain'))

    GMAIL_SMTP_PORT = 587
    session = smtplib.SMTP('smtp.gmail.com', GMAIL_SMTP_PORT)
    session.starttls() #enable security
    session.login(sender_address, sender_password)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')



mail_content = '''Hey Zayd, 
If you see this, please say hi
'''

sendEmail("z4tahir@uwaterloo.ca", mail_content, "HONK")