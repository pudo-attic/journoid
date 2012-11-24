import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

def notify(config, recipient, subject, message):
    msg = MIMEMultipart()
    mail_config = config.get('mail')
    msg['From'] = mail_config.get('sender')
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message))
    mailServer = smtplib.SMTP(mail_config.get("server"),
                        int(mail_config.get("port", 25)))
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    if mail_config.get('login'):
        mailServer.login(mail_config.get('login'),
                         mail_config.get('password'))
    mailServer.sendmail(mail_config.get('sender',
                        recipient,
                        msg.as_string())
    mailServer.close()
