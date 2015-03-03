'''
Created on Mar 3, 2015

@author: Autumn
'''
import requests
import logging
logger = logging.getLogger(__name__)

def stophook_sensu_client(url, user, password):
    
    """
    If the sensu client exsits, need to delete it.
    """
    timeout=5
    auth=None
    if user and password:
        auth = (user, password)
    
    try:
        ret = requests.get(url, auth=auth, timeout=timeout)
        if ret.status_code >= 200 and ret.status_code < 300:
            ret = requests.delete(url, auth=auth, timeout=timeout)
            return ret.status_code
        else:
            return ret.status_code
    except Exception as e:
        logger.exception(e)
        return 500
