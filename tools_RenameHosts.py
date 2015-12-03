#!/usr/bin/env python
# -*- coding : UTF-8 -*-

import re
import os,sys,datetime
import threading

class ThreadClass(threading.Thread):
  def run(self):
    now = datetime.datetime.now()
    print "%s over at time %s" % (self.getName(),now)


f = file(hostadd,r)
for line in f.readlines():
  ip = re.findall(d .d .d .d ,line)[0]
  host = line[15:].replace(" ","")
  cmd = "hostname %s && sed -i s/HOSTNAME=.*/HOSTNAME=\%s/g /etc/sysconfig/network" % (host,host)
  process = os.popen(ssh %s % ip "%s" % cmd).read()
  print process
  t = ThreadClass()
  t.start()
