from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip


@plann.testcase('Drive Stastics')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('durable-id'))
@htf.measures(htf.Measurement('location'))
@htf.measures(htf.Measurement('number-of-media-errors-1'))
@htf.measures(htf.Measurement('number-of-media-errors-2'))
@htf.measures(htf.Measurement('number-of-nonmedia-errors-1'))
@htf.measures(htf.Measurement('number-of-nonmedia-errors-2'))
@htf.measures(htf.Measurement('number-of-block-reassigns-1'))
@htf.measures(htf.Measurement('number-of-block-reassigns-2'))
@htf.measures(htf.Measurement('number-of-bad-blocks-1'))
@htf.measures(htf.Measurement('number-of-bad-blocks-2'))
@plann.plug(MSA_plug = MSA2060)
def drive_stats_collect(test, MSA_plug):
    
    keylist = ['html-response','key-response','durable-id','location','number-of-media-errors-1','number-of-media-errors-2','number-of-nonmedia-errors-1', 
             'number-of-nonmedia-errors-2','number-of-block-reassigns-1','number-of-block-reassigns-2','number-of-bad-blocks-1',
             'number-of-bad-blocks-2']
    
    results = {}
    for each in keylist:
        results[each] = []
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    
    results['html-response'] = MSA_plug.login()

    if results['html-response']:
        out = MSA_plug.get('disk-statistics','disk-statistics')
        if 'result' in out:
            results['key-response'] = out['result']
            if results['key-response']:
                disks = out['text']
                for disk in range(0,len(disks)):
                    for each in keylist[2:]:
                        if each in disks[disk]:
                            results[each].append(disks[disk][each])

    for each in keylist:
    
        test.measurements[each] = results[each]
    





    
    



    
