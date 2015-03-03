'''
Created on Jan 9, 2015

@author: Autumn
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from pyha.utils import exec_cmd

import logging
logger = logging.getLogger(__name__)


class StatusCheck:
    def __init__(self, command="ps -ef | grep '^sensu' | grep sensu-client > /dev/null"):
        self.cmd = command
    
    def check(self):
        logger.debug("Run command : %s" % self.cmd)
        return exec_cmd(self.cmd)
        

class HealthCheckHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        check = StatusCheck()
        (rc, out, error) = check.check()
        if rc==0:
            self.send_response(200)
        else:
            self.send_response(400)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if rc :
            self.wfile.write("OK")
        else:
            self.wfile.write("FAIL:%s" % error)
        return
    
class HealthCheckHttpServer(Thread):
    
    def __init__(self, port=10241):
        
        Thread.__init__(self)
        self.port = port
        self.server = HTTPServer(('', self.port), HealthCheckHandler)
        self.__closed__ = None
        
    def stop(self):
        self.server.server_close()
        self.__closed__ = True
    
        
    def is_stopped(self):
        return self.__closed__
    
        
    def run(self):
        
        try:
            
            logger.debug( 'Started httpserver on port %d'  % self.port )
            self.__closed__ = False
            self.server.serve_forever()
        
        except KeyboardInterrupt:
            logger.info( '^C received, shutting down the web server' )
            self.server.socket.close()
            self.__closed__ = True

        except Exception as e:
            logger.exception( "Exception : %s" % e )
    
## For testing
if __name__ == '__main__':
    server = HealthCheckHttpServer()
    server.start()
    server.join()
    
    

