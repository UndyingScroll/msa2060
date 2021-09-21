from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Controller Test')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('durable-id'))
@htf.measures(htf.Measurement('controller-id'))
@htf.measures(htf.Measurement('serial-number'))
@htf.measures(htf.Measurement('hardware-version'))
@htf.measures(htf.Measurement('mac-address'))
@htf.measures(htf.Measurement('disks'))
@htf.measures(htf.Measurement('status').equals(['Operational','Operational']))
@htf.measures(htf.Measurement('status-numeric'))
@htf.measures(htf.Measurement('fail-over-reason'))
@htf.measures(htf.Measurement('sc-fw'))
@htf.measures(htf.Measurement('vendor').equals(['HPE','HPE']))
@htf.measures(htf.Measurement('model').equals(['MSA 2060 FC','MSA 2060 FC']))
@htf.measures(htf.Measurement('part-number'))
@htf.measures(htf.Measurement('description'))
@htf.measures(htf.Measurement('revision'))
@htf.measures(htf.Measurement('health').equals(['OK','OK']))
@htf.measures(htf.Measurement('health-numeric').equals([0,0]))
@htf.measures(htf.Measurement('health-reason'))
@plann.plug(MSA_plug = MSA2060)
def controller_test(test, MSA_plug):
    
    keylist = ['key-response','html-response','durable-id','controller-id','serial-number','hardware-version',
            'mac-address','disks','status','status-numeric','fail-over-reason',
            'sc-fw','vendor','model','part-number','description','revision','health','health-numeric','health-reason']
    
    results = {}
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    results['html-response'] = MSA_plug.login()
    if results['html-response']:
        out = MSA_plug.get('controllers','controllers')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                controllers = out['text']
                for each in keylist[2:]:
                    if each in controllers[0]:
                        results[each] = [controllers[0][each],controllers[1][each]]

    for each in keylist:
    
        test.measurements[each] = results[each]


    
    



    
