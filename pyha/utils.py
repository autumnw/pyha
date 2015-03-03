'''
Created on Feb 13, 2015

@author: Autumn
'''
import os
import subprocess

def make_log_dir(log_dir):
    #log_dir = "/var/log/netmonitor/awswhitelist"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
def exec_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, close_fds=True, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    ret_code = p.returncode
    return (ret_code, out, err)