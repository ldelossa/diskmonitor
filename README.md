# Diskmonitor

Diskmonitor is a tool for monitoring disk io and alerting on events. The implementation uses python3.4, a hacked up version of collectd_iostat_python module, multi-threading (soon to be multiprocessing) and several internal queues.

### Functionality
  - Diskmonitor can be used as a long running program
  - Diskmonitor is capable of sending aggregated emails of alerts.
  - Diskmonitor is configured solely from a config.json file
  

### Architecture
Diskmonitor uses multi-threading and multiple queues as it's architectural foundation. Each monitor object is responsible for monitoring a disk. Each alert, metric, and email is sent to their own queus. Three queues exist in total (email, metrics, and alerts). Diskmonitor also provides a (limited for now) CLI. You are able to exit, dump your alerts, and dump your raw metrics

### Version
v1.2

### Usage
```
root# python3.4 /path/to/diskmonitor
```

### CLI
After running the diskmonitor package a cmd prompt will be presented. You have three options for now
 
| Command      | Purpose                        |
| ------------ | -------------------------------|
| exit         | exits program                  |
| dump_metrics | dumps raw metrics (not sorted) |
| dump_alerts  | dumps alerts (sorted)          |

There is also a 'help' command 

### Configuration
All configuration is done from config.json in the root of the pckage. You are able to remove metrics in "io_threshold" and they will not be checked. You are not able to add additional metrics at this point. I'm using a modified version of the collectd_iostat_python.py plugin. Once this is re-writen on my won, metrics choice will be possible. 

### ToDo
- Introduce thread manager, start, stop, exit monitors on command line
- Introduce some form of data persistence to make alerting more accurate
- Docuement CLI commands 
- RabbitMQ plugin
- Introduce daemon or detached mode for running as a service 
