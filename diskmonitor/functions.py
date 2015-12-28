from diskmonitor.monitor import Monitor
from diskmonitor.collectd_iostat_python import IOStat
from collections import defaultdict
from operator import itemgetter

def extract_disk_names():
    """
    Obtains list of disks on system that IOstat recognizes
    :return: List of disk objects
    """
    iostats = IOStat().get_diskstats()
    return [disk_name for disk_name in iostats]


def launch_monitor(disk_name, config_file, email_client, alerts_q, metrics_q):
    """
    Defines method for launching a Monitor. This is used as a target for the thread Class
    :param disk_name: String - a disk name returned by 'extract_disk_names()'
    :param config_file: - config.json
    :param email_client: diskmonitor.emailer.Emailer - shared email_client
    :param alerts_q: Collections.deque - shared alerts queue
    :param metrics_q: Collections.deque - shared metrics queue
    :return: None
    """
    monitor = Monitor(disk_name=disk_name,
                      config=config_file,
                      email_client=email_client,
                      alerts_que=alerts_q,
                      metrics_que=metrics_q)
    monitor.start_monitor()
    return


def dump_alerts(q, disk=None):
    """
    Dumps alerts orderd by device and date
    :param q: Collections.deque - shared alerts queue
    :param disk: String - optional disk filter
    :return: None
    """
    alerts = [alert for alert in q]
    alerts.sort(key=itemgetter('time'))

    dev_dict = defaultdict(list)
    for alert in alerts:
        dev_dict[alert['dev']].append(alert)

    if any([disk == d for d in extract_disk_names()]):
        print(disk)
        for i in dev_dict[disk]:
            print('     ', i)

    else:
        for key in dev_dict:
            print(key)
            for i in dev_dict[key]:
                print('     ', i)
    return

def dump_metrics(q):
    """
    Raw dump of metrics collected on metrics queue
    :param q: Collections.deque - shared metrics queue
    :return:
    """
    metrics = [metric for metric in q]
    for metric in metrics:
        print(metric)
    return