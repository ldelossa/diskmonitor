import psutil
from diskmonitor.emailer import Emailer
from diskmonitor import Monitor

def extract_disk_names():
    return [disk for disk in psutil.disk_io_counters(perdisk=True)]

def launch_monitor(*, disk_obj, read_time_threshold, write_time_threshold, poll_interval,
                   fromaddr, toaddr, username, password, smtp_server):
    email_client = Emailer(fromaddr=fromaddr,
                           toaddr=toaddr,
                           username=username,
                           password=password,
                           smtpserver=smtp_server)

    monitor = Monitor(disk_name=disk_obj,
                      read_time_threshold=read_time_threshold,
                      write_time_threshold=write_time_threshold,
                      poll_interval=poll_interval,
                      email_client=email_client)

    monitor.start_monitor()






