from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Drive Count')
@htf.measures(htf.Measurement('html-response').equals(True))
@htf.measures(htf.Measurement('key-response').equals(True))
@htf.measures(htf.Measurement('drive-expected'))
@htf.measures(htf.Measurement('drive-count'))
@htf.measures(htf.Measurement('drives-match').equals(True))
@plann.plug(MSA_plug = MSA2060)
def drive_count(test, MSA_plug):
    drive_count = 0
    results = {}
    results['drive_expected'] = _station['drive_qty']

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
                controllers = out['text'][0]
                if 'disks' in controllers:
                    results['drive_count'] = controllers['disks']
    
    test.measurements['html-response'] = results['html-response']
    test.measurements['key-response'] = results['key-response']
    test.measurements['drive-expected'] = results['drive_expected']
    test.measurements['drive-count'] = results['drive_count']
    test.measurements['drives-match'] = results['drive_expected'] == results['drive_count'] 