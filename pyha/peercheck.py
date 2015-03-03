'''
Created on Mar 3, 2015

@author: Autumn
'''
from threading import Thread
import requests
import time
import sys

import logging
logger = logging.getLogger(__name__)

class HeartbeatCheck(Thread):
    
    def __init__(self, remote_host, remote_port=10241, internval=10, timeout=3):
        Thread.__init__(self)
        self.url = "http://%s:%d" % (remote_host, remote_port)
        self.interval = internval
        self.remote_state = None
        self.timeout = timeout
        
        
    def run(self):
        while True:
            try:
                ret = requests.get(self.url, timeout=self.timeout)
                if ret.status_code == 200:
                    self.remote_state = True
                else:
                    self.remote_state = False
            except Exception as e:
                logger.exception("http get exception : %s" % e)
                self.remote_state = None
            finally:
                time.sleep(self.interval)
            
## For testing:
if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    h = HeartbeatCheck(host, port)
    h.start()
    while True:
        print "state : %s" % h.remote_state
        time.sleep(5)
        