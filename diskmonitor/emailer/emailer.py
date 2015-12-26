import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import deque
from time import sleep


class Emailer(object):
    def __init__(self, *, config, msg=None):
        self.fromaddr = config['email_config']['fromaddr']
        self.toaddrs = config['email_config']['toaddr']
        self.username = config['email_config']['username']
        self.password = config['email_config']['password']
        self.smtp_server = config['email_config']['smtp_server']
        self._msg = MIMEMultipart()
        self.body = None
        self._message_que = deque()

    def send_mail(self):
        self._msg['From'] = self.fromaddr
        self._msg['To'] = self.toaddrs
        self._msg['Subject'] = 'LS Alerting!'
        self._msg.attach(MIMEText(self.body, 'plain'))
        server = smtplib.SMTP(self.smtp_server)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        text = self._msg.as_string()
        server.sendmail(self.fromaddr, self.toaddrs, text)
        server.quit()

    def append_to_message_q(self, alert):
        self._message_que.append(alert)

    def set_message(self):
        messagelist = []
        while len(self._message_que) > 0:
            queued_message = self._message_que.pop()
            msg = '{} alerted on metric: {} on disk: {}! Current value: {}. Threshold: {} \n'.format(
                                                                                     queued_message['hostname'],
                                                                                     queued_message['metric'],
                                                                                     queued_message['dev'],
                                                                                     queued_message['current_value'],
                                                                                     queued_message['threshold'],
                                                                                        )
            messagelist.append(msg)
        self.body = " ".join(messagelist)
        print(self._msg)


    def start_client(self):
        while True:
            if len(self._message_que) >= 1:
                self.set_message()
                self.send_mail()
                print('sent email!')
                sleep(60)



