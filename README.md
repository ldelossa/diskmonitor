# Diskmonitor

Diskmonitor is a tool for monitoring disk io and alerting on events. The implementation uses python3.4, a hacked up version of collectd_iostat_python module, multi-threading (soon to be multiprocessing) and several internal queues.

### Requirements
  - Python3.4 (Python3 should work also)
  - Sysstat tools (provides iostat)

### Functionality
  - Diskmonitor can be used as a long running program
  - Diskmonitor is capable of sending aggregated emails of alerts.
  - Diskmonitor is configured solely from a config.json file
  - Diskmonitor now has a more robust CLI learn more below
  - Diskmonitor can now be ran as a daemon, and responds to SIGTERM signals appropriately
  

### Architecture
Diskmonitor uses multi-threading and multiple queues as it's architectural foundation. Each monitor object is responsible for monitoring a disk. Each alert, metric, and email is sent to their own queus. Three queues exist in total (email, metrics, and alerts). Diskmonitor also provides a (limited for now) CLI. You are able to exit, dump your alerts, and dump your raw metrics

### Version
v2.1

### Changes

 - Massive CPU utilization improvements. Now runs idle at 0.0% and runs with 3 monitors (tested) at 0.3%
 - Fixed bug in emailer class
 - various data structure improvements.

### Usage
Be sure to fill in the email section in config.json or diskmonitor will not start!!

Start in interactive mode

```
root# python3.4 /path/to/diskmonitor
```

Start in detached mode (daemon) pid file writen to /tmp/diskmonitor.pid (to avoid any permissions issues with writing PID)
```
root# python3.4 /path/to/diskmonitor --detached | -d
```

Diskmonitor will respond correctly to SIGTERM signals and remove it's PID file. 


### CLI
After running the diskmonitor package a cmd prompt will be presented. You have three options for now
 
| Command      | Purpose                         | Arguments
| ------------ | --------------------------------|---------------------------------------------------------------------|
| exit         | exits program                   | None								       |
| dump_metrics | dumps raw metrics (not sorted)  | None								       | 
| dump_alerts  | dumps alerts (sorted)           | Disk name returned from list_disks				       |
| dump_monitors| displays active monitors        | None								       |
| launch_monitor | launches a monitor            | disk name returned from list_disks or all			       |
| stop_monitor | stops a monitor                 | Requires a disk name                                                |
| list_disks   | lists disks available to monitor| None								       |

There is also a 'help' command 

### Examples:

```
(Cmd) list_disks
['sda', 'sdc', 'sdd', 'sdb']
(Cmd) launch_monitor sda
(Cmd) dump_monitors
Number of monitors running 1 

{'sda': <Thread(sda, started daemon 139895737190144)>}
(Cmd) stop_monitor sda
(Cmd) dump_monitors
Number of monitors running 0 

(Cmd) 
```

diskmonitor will not let you monitor the same disks twice.

```
(Cmd) launch_monitor all
(Cmd) 
Monitors already running for all disks
(Cmd) exit
```


### Configuration
All configuration is done from config.json in the root of the pckage. You are able to remove metrics in "io_threshold" and they will not be checked. You are not able to add additional metrics at this point. I'm using a modified version of the collectd_iostat_python.py plugin. Once this is re-writen on my won, metrics choice will be possible. 

### ToDo
- ~~Introduce thread manager, start, stop, exit monitors on command line~~
- re-write metrics collection to not depend on IOstat or collectd plugin 
- Introduce some form of data persistence to make alerting more accurate
- Docuement CLI commands 
- RabbitMQ plugin
<<<<<<< HEAD
- Introduce daemon or detached mode for running as a service 

Project has been tested on Ubuntu 14.04 and CentOS-7
=======
- ~~Introduce daemon or detached mode for running as a service~~
- Incorporate disk space monitoring
- Move to multi-processing (see if more cpu efficient first)
- Efficiently sort metrics dump
- Add queue max's to json configuration
- Heavy CPU optimization (been looking for a reason to look at Cython
>>>>>>> thread_manager
