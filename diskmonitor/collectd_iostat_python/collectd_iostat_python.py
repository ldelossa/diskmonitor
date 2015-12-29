#!/usr/bin/env python
# coding=utf-8
#
# collectd-iostat-python
# ======================
#
# Collectd-iostat-python is an iostat plugin for collectd that allows you to
# graph Linux iostat metrics in Graphite or other output formats that are
# supported by collectd.
#
# https://github.com/powdahound/redis-collectd-plugin
#   - was used as template
# https://github.com/keirans/collectd-iostat/
#   - was used as inspiration and contains some code from
# https://bitbucket.org/jakamkon/python-iostat
#   - by Kuba Kończyk <jakamkon at users.sourceforge.net>
#

import signal
import string
import subprocess
import sys


__version__ = '0.0.3'
__author__ = 'denis.zhdanov@gmail.com'
# I have altered this file in order to work with diskmonitor
# all original work is to be credited to the above author

class IOStatError(Exception):
    pass


class CmdError(IOStatError):
    pass


class ParseError(IOStatError):
    pass


class IOStat(object):
    def __init__(self, path='/usr/bin/iostat', interval=2, count=2, disks=[]):
        self.path = path
        self.interval = interval
        self.count = count
        self.disks = disks

    def parse_diskstats(self, input):
        """
        Parse iostat -d and -dx output.If there are more
        than one series of statistics, get the last one.
        By default parse statistics for all avaliable block devices.

        @type input: C{string}
        @param input: iostat output

        @type disks: list of C{string}s
        @param input: lists of block devices that
        statistics are taken for.

        @return: C{dictionary} contains per block device statistics.
        Statistics are in form of C{dictonary}.
        Main statistics:
          tps  Blk_read/s  Blk_wrtn/s  Blk_read  Blk_wrtn
        Extended staistics (available with post 2.5 kernels):
          rrqm/s  wrqm/s  r/s  w/s  rsec/s  wsec/s  rkB/s  wkB/s  avgrq-sz \
          avgqu-sz  await  svctm  %util
        See I{man iostat} for more details.
        """
        # made edits to original code here to output string values instead of bytes
        dstats = {}
        dsi = input.rfind('Device:'.encode())
        if dsi == -1:
            raise ParseError('Unknown input format: %r' % input)

        ds = input[dsi:].splitlines()
        hdr = ds.pop(0).split()[1:]

        for d in ds:
            if d:
                d = d.split()
                dev = d.pop(0)
                if (dev.decode('utf-8') in self.disks) or not self.disks:
                    dstats[dev.decode('utf-8')] = dict([(k.decode('utf-8'), float(v)) for k, v in zip(hdr, d)])
        return dstats

    def sum_dstats(self, stats, smetrics):
        """
        Compute the summary statistics for chosen metrics.
        """
        avg = {}

        for disk, metrics in stats.iteritems():
            for mname, metric in metrics.iteritems():
                if mname not in smetrics:
                    continue
                if mname in avg:
                    avg[mname] += metric
                else:
                    avg[mname] = metric

        return avg

    def _run(self, options=None):
        """
        Run iostat command.
        """
        close_fds = 'posix' in sys.builtin_module_names
        args = '%s %s %s %s %s' % (
            self.path,
            ''.join(options),
            self.interval,
            self.count,
            ' '.join(self.disks))

        return subprocess.Popen(
            args,
            bufsize=1,
            shell=True,
            stdout=subprocess.PIPE,
            close_fds=close_fds,
            )

    @staticmethod
    def _get_childs_data(child):
        """
        Return child's data when avaliable.
        """
        (stdout, stderr) = child.communicate()
        ecode = child.poll()

        if ecode != 0:
            raise CmdError('Command %r returned %d' % (child.cmd, ecode))

        return stdout

    def get_diskstats(self):
        """
        Get all avaliable disks statistics that we can get.
        """
        dstats = self._run(options=['-kd'])
        extdstats = self._run(options=['-kdx'])
        dsd = self._get_childs_data(dstats)
        edd = self._get_childs_data(extdstats)
        ds = self.parse_diskstats(dsd)
        eds = self.parse_diskstats(edd)

        for dk, dv in ds.items():
            if dk in eds:
                ds[dk].update(eds[dk])

        return ds

# io = IOStat(disks=['sda'])
# ds = io.get_diskstats()
# print(ds)





