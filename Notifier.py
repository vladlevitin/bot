import smtplib, ssl
import requests
port = 465  # For SSL
smtp_server = "smtp-mail.outlook.com"


class Notifier:
    def __init__(self, sender_login, sender_password):
        self.receiver_list = []
        self.sender_login = sender_login
        self.sender_password = sender_password

    def add_receiver(self, mail):
        self.receiver_list.append(mail)

    def delete_receiver(self, mail):
        self.receiver_list.remove(mail)

    def send_mail(self, message):
        """context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(self.sender_login, self.sender_password)
            for receiver_login in self.receiver_list:
                server.sendmail(self.sender_login, receiver_login, message)
        print("Message successfully sent")"""

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.sender_login, self.sender_password)

            for receiver_login in self.receiver_list:
               smtp.sendmail(self.sender_login, receiver_login, message)
        print("Message successfully sent")

