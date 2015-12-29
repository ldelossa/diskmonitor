import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import deque
from time import sleep


class Emailer(object):
    """
    Email client object. Receives messages of email queue, waits for interval to be up, concatenates all emails
    on queue into one email and sends. This client is shared between each monitor. Each monitor has access to it's queue
    """
    def __init__(self, *, config, msg=None):
        self.body = None
        self._msg = MIMEMultipart()
        self._message_que = deque()
        self._config = config

    def send_mail(self):
        """
        Send email.
        Looks at config.json for email configuration information. Crafts email using Mime multi-part method
        :return:
        """
        self._msg['From'] = self._config['email_config']['fromaddr']
        self._msg['To'] = self._config['email_config']['toaddr']
        self._msg['Subject'] = self._config['email_config']['subject']
        self._msg.attach(MIMEText(self.body, 'plain'))
        server = smtplib.SMTP(self._config['email_config']['smtp_server'])
        server.ehlo()
        server.starttls()
        server.login(self._config['email_config']['username'], self._config['email_config']['password'])
        server.sendmail(self._config['email_config']['fromaddr'], self._config['email_config']['toaddr'], self._msg.as_string())
        server.quit()

    def append_to_message_q(self, alert):
        """
        Appends alert to email queue. Used by monitors
        :param alert:
        :return:None
        """
        self._message_que.append(alert)

    def set_message(self):
        """
        Concatenates multiple alerts on the email_queue into a summary message.
        :return:None
        """
        message_list = []

        while len(self._message_que) > 0:
            queued_message = self._message_que.pop()
            msg = 'Host: {} alerted on metric: {} on disk: {}! Current value: {}. Threshold: {} \n'.format(
                                                                                     queued_message['hostname'],
                                                                                     queued_message['metric'],
                                                                                     queued_message['dev'],
                                                                                     queued_message['current_value'],
                                                                                     queued_message['threshold'],
                                                                                        )
            message_list.append(msg)

        self.body = " ".join(message_list)

    def start_client(self):
        """
        Starts the long-running email client. Monitors its queue, if there are items on the queue, set messages
        and send, sleep until send_interval is up.
        :return:
        """
        while True:
            if len(self._message_que) >= 1:
                self.set_message()
                self.send_mail()
                # print('sent email!')
                sleep(self._config['email_config']['send_interval'])



