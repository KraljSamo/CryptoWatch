import os
import smtplib, ssl

from dotenv import load_dotenv

from email.mime.text import MIMEText
import datetime

class Notifier:

    def __init__(self, smtp='smtp-mail.outlook.com', port=587):
        load_dotenv()
        self.username = os.getenv('EMAIL_USERNAME')
        self.password = os.getenv('PASSWORD')
        self.target = os.getenv('TARGET')
        self.smtp = smtp
        self.port = port


    def send_email(self, subject, message):

        with smtplib.SMTP(host=self.smtp, port=self.port) as server:
            
            server.starttls()
            server.login(self.username, self.password)

            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = self.target

            server.send_message(msg)
    
    def create_update_message(self, notifications):
        
        sorted_by_importance = sorted(notifications, reverse=True)

        subject = '[CRYPTO] ' + ' '.join((str(e[1]) + ' : ' + str(round((e[0] - 1)*100, 2)) + '%' for e in sorted_by_importance[:3]))

        message = """"""

        for change, coin, date_past, price_past, date_now, price_now in sorted_by_importance:

            message += '\n'
            message += f'{coin} -> PRICE CHANGE -> {change} in the last {date_now - date_past}\n \n'
            message += f'{coin} -- {date_past} -- {price_past} \n' 
            message += f'{coin} -- {date_now} -- {price_now} \n \n' 

        print(subject)
        print(message)

        self.send_email(subject, message)

if __name__ == '__main__':
    notifier = Notifier('smtp-mail.outlook.com', 587)
    # notifier.send_email('This is a test email!', 'Test email - do not delete')
    notifier.create_update_message([[1.1, 'bitcoin', datetime.datetime.now(), 10000, datetime.datetime.now(), 11000]])