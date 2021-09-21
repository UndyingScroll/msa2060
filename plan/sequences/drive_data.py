from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Drive Health Test')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('durable-id'))
@htf.measures(htf.Measurement('slot'))
@htf.measures(htf.Measurement('location'))
@htf.measures(htf.Measurement('serial-number'))
@htf.measures(htf.Measurement('vendor'))
@htf.measures(htf.Measurement('model'))
@htf.measures(htf.Measurement('revision'))
@htf.measures(htf.Measurement('error-occured').equals(False))
@htf.measures(htf.Measurement('error'))
@htf.measures(htf.Measurement('size'))
@htf.measures(htf.Measurement('temperature-numeric'))
@htf.measures(htf.Measurement('power-on-hours'))
@htf.measures(htf.Measurement('power-on-hours-valid').equals(True))
@htf.measures(htf.Measurement('architecture'))
@htf.measures(htf.Measurement('ssd-life-left'))
@htf.measures(htf.Measurement('ssd-life-left-numeric'))
@htf.measures(htf.Measurement('health'))
@htf.measures(htf.Measurement('health-valid').equals(True))
@htf.measures(htf.Measurement('health-numeric'))
@htf.measures(htf.Measurement('health-reason'))
@htf.measures(htf.Measurement('health-recommendation'))
@plann.plug(MSA_plug = MSA2060)
def drive_health(test, MSA_plug):
    
    keylist = ['key-response','html-response','durable-id','slot','location','serial-number','vendor','model',
            'revision','error','size','temperature-numeric','power-on-hours',
            'health','health-numeric','health-reason','health-recommendation',
            'architecture', 'ssd-life-left','ssd-life-left-numeric']
    
    results = {}
    for each in keylist:
        results[each] = []
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    darray = []
    results['html-response'] = MSA_plug.login()
    
    if results['html-response']:
        out = MSA_plug.get('disks','drives')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                disks = out['text']
                for disk in range(0,len(disks)):
                    for each in keylist[2:]:
                        if each in disks[disk]:
                            results[each].append(disks[disk][each])
    
    if test.test_record.metadata['test_description'] == 'B Stock':
        test.measurements['power-on-hours-valid'] = all([x < 43800 for x in results['power-on-hours']])
    else:
        test.measurements['power-on-hours-valid'] = all([x < 2190 for x in results['power-on-hours']])

    test.measurements['health-valid'] = all([x == 'OK' for x in results['health']])
    test.measurements['error-occured'] = all(results['error'])
   
    for each in keylist:
    
        test.measurements[each] = results[each]
    





    
    



    
