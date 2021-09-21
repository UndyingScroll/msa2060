from spintop_openhtf import TestPlan,  conf
import time
from plan.station import _station,ip_addr,port,username,password,timeout,sudo, versions
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.ping_plug import PingPlug
from ..SAN_Plan import plann


@plann.testcase('Ping Test @ 10.0.0.2', repeat_limit = 3)
@htf.measures(htf.Measurement('ping_response').equals(True))
@plann.plug(net_plug=PingPlug)
def ping_test(test, net_plug):
    data = False
    data = net_plug.ping(ip_addr)
    if data == False:
        time.sleep(30)
        return PhaseResult.REPEAT
         
    test.measurements.ping_response = data
