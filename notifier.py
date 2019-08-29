import os
import smtplib, ssl

from dotenv import load_dotenv

from email.mime.text import MIMEText

class Notifier:

    def __init__(self, smtp, port):
        load_dotenv()
        self.username = os.getenv('EMAIL_USERNAME')
        self.password = os.getenv('PASSWORD')
        self.target = os.getenv('TARGET')
        self.smtp = smtp
        self.port = port


    def send_email(self, message, subject):

        with smtplib.SMTP(host=self.smtp, port=self.port) as server:
            
            server.starttls()
            server.login(self.username, self.password)

            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = self.target

            server.send_message(msg)

notifier = Notifier('smtp-mail.outlook.com', 587)
notifier.send_email('This is a test email!', 'Test email - do not delete')