import os, time, sys
from os import path
import yaml
import openhtf as htf
from openhtf import PhaseResult
from openhtf.plugs.user_input import UserInput
#from openhtf.util import conf
from openhtf_docx_report import docx_report_callback
from spintop_openhtf.callbacks import station_server
import webbrowser
from spintop_openhtf import TestPlan,  conf
from spintop_openhtf.util.markdown import markdown
from plan.forms import DUT_FORM_LAYOUT, SETUP_FORM_LAYOUT, DONE_FORM_LAYOUT
from openhtf.output.callbacks import json_factory
from copy import deepcopy
from plan.plugs.GreetPlug import GreetPlug
from plan.station import _station,ip_addr, versions
from plan.SAN_Plan import plann
from plan.callbacks.openhtf_docx_report import docx_report_callback
#from plan.callbacks.sql_records_callback import sql_reports_callback


# sequences in order to be appended
from plan.sequences.logging import run_info
from plan.sequences.user import user_setup
from plan.sequences.waiting import waiting
from plan.sequences.network import network_test
from plan.sequences.system import system_test
from plan.sequences.controller import controller_test
from plan.sequences.fans import fan_test
from plan.sequences.power import power_test
from plan.sequences.drive_count import drive_count
from plan.sequences.drive_data import drive_health
from plan.sequences.drive_size import drive_size_test
from plan.sequences.drive_stats import drive_stats_collect
from plan.sequences.events import clear_events
from plan.sequences.splash_page import complete




HERE = os.path.abspath(os.path.dirname(__file__))


@plann.trigger('IOX-SAN-2U-CORE Drive Health')
@plann.plug(greet=GreetPlug)
def DUT(test, greet):
    
    response = greet.prompt_tester_information()

   
    if 'serialnumber' not in response:
        return PhaseResult.REPEAT
    
    if 'dropdown' in response:
          
        test.test_record.metadata['test_description'] = response['dropdown']
    else:
        test.test_record.metadata['test_description'] = 'A stock'
    if 'customer' in response:
        _station['customer'] = response['customer']
    if 'ponumber' in response:
        _station['PO_number'] = response['ponumber']
    if 'drive' in response:
        _station['drive'] = response['drive']
    if 'drive_qty' in response:
        _station['drive_qty'] = int(response['drive_qty'])

    test.test_record.metadata['test_version'] ='1.0'
    test.test_record.metadata['user_id'] = 'default'
    test.test_record.metadata['path'] = 'c:\\MSA2060\\Reports\\'
    
    
    test.dut_id = response['serialnumber']
    
    





def nowtime():
    return int(round(time.time() * 1000)) 



def main():
    
    
    plann.add_callbacks(docx_report_callback)
    #plann.add_callbacks(sql_reports_callback)
    conf.load(station_server_port='4444')
    plann.run()


if __name__ == '__main__':
  main()
