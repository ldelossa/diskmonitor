import smtplib


class Emailer(object):
    def __init__(self, *, config, msg=None):
        self.fromaddr = config['email_config']['fromaddr']
        self.toaddrs = config['email_config']['toaddr']
        self.username = config['email_config']['username']
        self.password = config['email_config']['password']
        self.smtp_server = config['email_config']['smtp_server']
        self.msg = msg

    def send_mail(self):
        server = smtplib.SMTP(self.smtp_server)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg)
        server.quit()

    def set_message(self, alert):
        self.msg = '{} alerted on metric: {} on disk: {}! Current value: {}. Threshold: {}'.format(
                                                                                      alert['hostname'],
                                                                                      alert['metric'],
                                                                                      alert['dev'],
                                                                                      alert['current_value'],
                                                                                      alert['threshold'],
                                                                                        )
