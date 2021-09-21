from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip

@plann.testcase('Clear Events Log')
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('status').equals(True))
@plann.plug(MSA_plug = MSA2060)
def clear_events(test, MSA_plug):
       
    results = {}
    
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    
    results['html-response'] = MSA_plug.login()
    command = ['clear','events','both']
    set = MSA_plug.set(command)
    test.logger.info(set['text'])
    results['status'] = set['result']
        
    test.measurements['html-response'] = results['html-response']
    test.measurements['status'] = results['status']
    





    
    



    
