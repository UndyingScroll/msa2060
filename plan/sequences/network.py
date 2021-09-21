from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Network Parameter Test')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('object-name'))
@htf.measures(htf.Measurement('link-speed'))
@htf.measures(htf.Measurement('health').equals(['OK','OK']))
@htf.measures(htf.Measurement('health-numeric').equals([0,0]))
@htf.measures(htf.Measurement('health-reason'))
@htf.measures(htf.Measurement('health-recommendation'))
@plann.plug(MSA_plug = MSA2060)
def network_test(test, MSA_plug):
    
    keylist = ['key-response','html-response','object-name', 'link-speed', 'health', 'health-numeric', 'health-reason', 'health-recommendation' ]
    
    results = {}
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    results['html-response'] = MSA_plug.login()
    if results['html-response']:
        out = MSA_plug.get('network-parameters','network-parameters')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                controllers = out['text']
                for each in keylist[2:]:
                    if each in controllers[0]:
                        results[each] = [controllers[0][each],controllers[1][each]]

    for each in keylist:
    
        test.measurements[each] = results[each]


    
    



    
