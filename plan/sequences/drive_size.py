from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip

drive_map = { "IOX-SAN-2U-6TB": '6.0TB', "IOX-SAN-2U-8TB": '8.0TB', "IOX-SAN-2U-10TB": '10.0TB',
                "IOX-SAN-2U-12TB": '12.0TB', "IOX-SAN-2U-14TB" : '14.0TB', "IOX-SAN-2U-16TB": '16.0TB',
                "IOX-SAN-2U-18TB": '18.0TB', "IOX-SAN-2U-72TB" : '72.0TB', "IOX-SAN-2U-96TB": '96.0TB', 
                "IOX-SAN-2U-120TB": '120.0TB', "IOX-SAN-2U-144TB" : '144.0TB', "IOX-SAN-2U-168TB": '168.0TB', 
                "IOX-SAN-2U-192TB": '192.0TB', "IOX-SAN-2U-216TB": '216.0TB'}

@plann.testcase('Drive Size Test')
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('durable-id'))
@htf.measures(htf.Measurement('slot'))
@htf.measures(htf.Measurement('location'))
@htf.measures(htf.Measurement('size-expected'))
@htf.measures(htf.Measurement('size'))
@htf.measures(htf.Measurement('size-valid').equals(True))
@htf.measures(htf.Measurement('drive-expected'))
@htf.measures(htf.Measurement('storage-size-set').equals('TB'))
@htf.measures(htf.Measurement('storage-size-units').equals('AUTO'))
@plann.plug(MSA_plug = MSA2060)
def drive_size_test(test, MSA_plug):
    
    keylist = ['key-response','html-response','durable-id','slot','location','size']
    
    results = {}
    for each in keylist:
        results[each] = []
    if onfailskip(test) == False:
        return PhaseResult.SKIP   
    MSA_plug.ip = ip_addr
    MSA_plug.username = username
    MSA_plug.password = password
    results['drive-expected'] = _station['drive']
    results['size-expected'] = drive_map.get(_station['drive'], 'None')
    results['html-response'] = MSA_plug.login()
    command = ['set','cli-parameters','storage-size-units','TB']
    set_TB = MSA_plug.set(command)
    if set_TB['result']:
        out = MSA_plug.get('cli-parameters','cli-parameters')
        if out.get('result', False):
            results['storage-size-set']=out['text'][0]['storage-size-units'].upper()

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

    command = ['set','cli-parameters','storage-size-units','AUTO']
    set_TB = MSA_plug.set(command)
    if set_TB['result']:
        out = MSA_plug.get('cli-parameters','cli-parameters')
        if out.get('result', False):
            results['storage-size-units']=out['text'][0]['storage-size-units'].upper()

    test.measurements['drive-expected'] = results['drive-expected']
    test.measurements['size-expected'] = results['size-expected']
    test.measurements['size-valid'] = all([ x == results['size-expected'] for x in results['size']])
    test.measurements['storage-size-set'] = results['storage-size-set']
    test.measurements['storage-size-units'] = results['storage-size-units']
    for each in keylist:
    
        test.measurements[each] = results[each]
    





    
    



    
