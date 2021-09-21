from logging import raiseExceptions
import os, time
from spintop_openhtf import TestPlan,  conf
from ..plugs.ping_plug import PingPlug
from ..plugs.REST_Plug import MSA2060
from ..SAN_Plan import plann
from plan.station import _station,ip_addr,username,password
from tenacity import Retrying, RetryError, retry, stop_after_attempt, stop_after_delay, wait_fixed
import openhtf as htf


@retry(stop=(stop_after_delay(360)), wait=wait_fixed(10))
def check_for_ping():

    pinger = PingPlug()
    data = False
    data = pinger.ping(ip_addr)
    print(data)
    if data == False:
        print('ping failed')
        raise Exception
    else:
        print('ping passed')
        return True


@retry(stop=(stop_after_delay(120)), wait=wait_fixed(10))
def check_for_rest():


    data = False
    t = MSA2060()
    t.ip = ip_addr
    t.username = username
    t.password = password
    out = t.login()
    print(out)
    if out == False:
        print('rest connect failed')
        raise Exception
    else:
        print('rest connect passed')
        return True

@plann.testcase('Waiting for UUT to boot...5m 30s')
@htf.measures(htf.Measurement('ping_response').equals(True))
@htf.measures(htf.Measurement('html_response').equals(True))
def waiting(test):
    ping, html = False, False
    
    try:
        ping = check_for_ping()
    except RetryError as e:
        test.logger.info("Ping error: {}".format(e))
    try:
        html = check_for_rest()
    except RetryError as e:
        test.logger.info("HTTP REST error: {}".format(e))

    
    test.measurements.ping_response = ping
    test.measurements.html_response = html

