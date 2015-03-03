'''
Created on Mar 3, 2015

@author: Autumn
'''
from pyha.healthcheckserver import HealthCheckHttpServer
import json
from pyha.peercheck import HeartbeatCheck
import time
from pyha.utils import exec_cmd
import requests
import logging
from pyha.stophooks import stophook_sensu_client
logger = logging.getLogger(__name__)

class Pyha:
    def __init__(self, config="../conf/pyha.json"):
        with open(config, 'rt') as f:
            self.config = json.load(f)
        logger.info("config : %r" % self.config)
        
    def start_service(self, service):
        service_name = service['name']
        cmd = "service %s status" % service_name
        (ret_code, out, err) = exec_cmd(cmd)
        if ret_code == 0:
            logger.info("service %s is running, skip..." %  service_name)
        else:
            cmd = "service %s start" % service_name
            (ret_code, out, err) = exec_cmd(cmd)
            if ret_code == 0:
                logger.info("start service %s successfully" % service_name)
            else:
                logger.error("start service %s failed : %s" % (service_name, err))
                
                
    def run_stop_hook(self, hook, is_master):
        logger.info("run stop hook : %r" % hook)
        hook_type = hook['type']
        if hook_type == 'stophook_sensu_client':
            client = self.config['peer']['master']
            if is_master:
                client = self.config['peer']['slave']
                
            url = "%s/%s" % (hook['url'], client)

            user = hook.get('user', None)
            password = hook.get('password', None)
            stophook_sensu_client(url, user, password)
        else:
            logger.error("Unsupported stop hook type : %s" % hook_type)
    
    def stop_service(self, service):
        service_name = service['name']
        #stop_hook = service.get('stop_hook', None)
        cmd = "service %s status" % service_name
        (ret_code, out, err) = exec_cmd(cmd)
        if ret_code != 0:
            logger.info("service %s is not running, skip..." %  service_name)
        else:
            cmd = "service %s stop" % service_name
            (ret_code, out, err) = exec_cmd(cmd)
            if ret_code == 0:
                logger.info("stop service %s successfully" % service_name)
            else:
                logger.error("stop service %s failed : %s" % (service_name, err))
        
         
    def run(self):
        server = HealthCheckHttpServer()
        server.start()
        
        is_master = self.config['is_master']
        remote_host = self.config['peer']['master']
        if is_master:
            remote_host = self.config['peer']['slave']
        
        peer = HeartbeatCheck(remote_host)
        peer.start()
        
        time.sleep(3)
        
        service = self.config['service']
        hook = service.get('stop_hook', None)
        
        #stop_hook_was_run = False
        
        while True:
            remote_state = peer.remote_state
            if is_master:
                logger.debug("I am master, remote_state=%r" % remote_state)
                if (remote_state == None) or (remote_state == False):
                    self.start_service(service)
                    self.run_stop_hook(hook, is_master)

                    
            else:
                logger.debug("I am slave, remote_state=%r" % remote_state)
                if (remote_state == None) or (remote_state == False):
                    self.start_service(service)
                    self.run_stop_hook(hook, is_master)
                else:
                    self.stop_service(service)
                
            time.sleep(10)
        

        
        
    
