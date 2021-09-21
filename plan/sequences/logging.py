from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station,ip_addr,port,username,password, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from ..process import onfailskip



@plann.testcase('Run Info')
@htf.measures(htf.Measurement('Purchase Order'))
@htf.measures(htf.Measurement('Customer'))
@htf.measures(htf.Measurement('Part Number'))
@htf.measures(htf.Measurement('Disk Part Number'))
@htf.measures(htf.Measurement('Disk Quantity'))
def run_info(test):
    #_station = {'customer':'None','PO_number':'None', 'enclosure':'IOX-SAN-2U-CORE','drive':'None','drive_qty':0}  

    results = {}
    results['Purchase Order'] = _station['PO_number']
    results['Customer'] = _station['customer']
    results['Part Number'] = _station['enclosure']
    results['Disk Part Number'] = _station['drive']
    results['Disk Quantity'] = _station['drive_qty']


    for each in results:
        test.measurements[each] = results[each]