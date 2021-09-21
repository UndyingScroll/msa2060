from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Fans Test')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('durable-id'))
@htf.measures(htf.Measurement('name'))
@htf.measures(htf.Measurement('location'))
@htf.measures(htf.Measurement('status-ses').equals(['OK','OK']))
@htf.measures(htf.Measurement('status').equals(['Up','Up']))
@htf.measures(htf.Measurement('status-ses-numeric').equals([1,1]))
@htf.measures(htf.Measurement('position'))
@htf.measures(htf.Measurement('position-numeric'))
@htf.measures(htf.Measurement('health').equals(['OK','OK']))
@htf.measures(htf.Measurement('health-numeric').equals([0,0]))
@htf.measures(htf.Measurement('health-reason'))
@plann.plug(MSA_plug = MSA2060)
def fan_test(test, MSA_plug):
    
    keylist = ['key-response','html-response','durable-id','name','location','status-ses','status-ses-numeric','status',
            'position','position-numeric','health','health-numeric','health-reason']
    
    results = {}
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    results['html-response'] = MSA_plug.login()
    if results['html-response']:
        out = MSA_plug.get('fans','fan')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                fans = out['text']
                for each in keylist[2:]:
                    if each in fans[0]:
                        results[each] = [fans[0][each],fans[1][each]]

    for each in keylist:
    
        test.measurements[each] = results[each]


    
    



    
