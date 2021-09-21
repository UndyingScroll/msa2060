from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('System Test')
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('object-name'))
@htf.measures(htf.Measurement('system-name'))
@htf.measures(htf.Measurement('midplane-serial-number'))
@htf.measures(htf.Measurement('product-id').equals('MSA 2060 FC'))
@htf.measures(htf.Measurement('health').equals('OK'))
@htf.measures(htf.Measurement('health-numeric'))
@htf.measures(htf.Measurement('health-reason'))
@htf.measures(htf.Measurement('other-MC-status'))
@htf.measures(htf.Measurement('other-MC-status-numeric'))
@plann.plug(MSA_plug = MSA2060)
def system_test(test, MSA_plug):
    keylist = ['key-response','html-response','object-name','system-name','midplane-serial-number','product-id',
            'health','health-numeric','health-reason','other-MC-status','other-MC-status-numeric']
    results = {}
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password

    results['html-response'] = MSA_plug.login()
    if results['html-response']:
        out = MSA_plug.get('system','system')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                system = out['text'][0]
                for each in keylist[2:]:
                    results[each] = system[each]
    
 
    for each in keylist:
        test.measurements[each] = results[each]