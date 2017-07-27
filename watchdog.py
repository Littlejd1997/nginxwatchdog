import os
import sys
import requests
import json
import time
from daemon import Daemon
from time import sleep
class watchdog(Daemon):
  logfile = "<NGINX ACCESS LOG>""
  def run(self):
    file = open(self.logfile,'r')
    file.seek(0,2)
    while True:
      try:
       f = open(self.logfile,'r')
       if (os.fstat(file.fileno()).st_ino != os.fstat(f.fileno()).st_ino):
        f.seek(0,2)
        file = f
      except:
        sleep(1)
      line = file.readline()
      if len(line) > 0:
        try:
         data = json.loads(line)
         f = open(data['request_body_file'],'r')
         print( line)
         data['request_body'] = f.read()
         f.close()
         os.remove(data['request_body_file'])
         del data['request_body_file']
         line = json.dumps(data)
         print( line)
         r = requests.post('<URL FOR LAMBDA VIA API GATEWAY>',data=line)
        except:
         sleep(1)
      sleep(1)
if __name__ == "__main__":
         watchdog("/tmp/watchdoglogger.pid").run()
def start():
        watchdog("/tmp/watchdoglogger.pid").start()
def stop():
        watchdog("/tmp/watchdoglogger.pid").stop()
def restart():
        watchdog("/tmp/watchdoglogger.pid").restart()
