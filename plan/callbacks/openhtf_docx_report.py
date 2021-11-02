from openhtf.output.callbacks import json_factory
from pathlib import Path
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
import datetime, time, os
import matplotlib.pyplot as plt
from matplotlib import cm
from math import log10

def docx_report_callback(test_record):
    
    template_file = 'template.docx'  
    template = {}
    record_dict = json_factory.OutputToJSON(sort_keys = True).convert_to_dict(test_record)
    
    phase_no = 0
    test_execution_id = None
    template['dut_id'] = record_dict['dut_id']
    if 'test_name' in record_dict['metadata']:
        template['test_name'] = record_dict['metadata']['test_name']
    if 'test_version' in record_dict['metadata']:
        template['test_version'] = record_dict['metadata']['test_version']
    if 'test_description' in record_dict['metadata']:
        template['test_description'] = record_dict['metadata']['test_description']
    if 'path' in record_dict['metadata']:
        path = record_dict['metadata']['path']
    else:
        path = os.getcwd()
    template['test_date'] = datetime.datetime.fromtimestamp(record_dict['start_time_millis']/1000.0)
    
    if 'user_id' in record_dict['metadata']:
        template['user_id'] = record_dict['metadata']['user_id']
    
    test_duration = record_dict['end_time_millis']-record_dict['start_time_millis']
    template['passed']= 0
    template['failed'] = 0
    template['error'] = 0
    template['timeout'] = 0
    template['aborted'] = 0
    template['test_duration'] = test_duration
    template['test_outcome'] = record_dict['outcome']
    template['row_contents'] = []
    for phase in record_dict['phases']:

        template['row_contents'].append({})
        template['row_contents'][phase_no]['phase'] = phase_no+1
        template['row_contents'][phase_no]['name'] = phase['name']
        template['row_contents'][phase_no]['outcome'] = phase['outcome']
        if 'PASS' in phase['outcome']:
            template['passed'] += 1
        elif 'ERROR' in phase['outcome']:
            template['error'] += 1
        elif 'TIMEOUT' in phase['outcome']:
            template['timeout'] += 1
        elif 'FAIL' in phase['outcome']:
            template['failed'] += 1
        elif 'ABORT' in phase['outcome']:
            template['aborted'] += 1
        phase_duration = phase['end_time_millis']-phase['start_time_millis']
        template['row_contents'][phase_no]['duration'] = phase_duration
        template['row_contents'][phase_no]['notes'] = 'None'
        phase_no += 1
    phase_no = 0
    table_no = 0
    template['phase_contents'] = []

    for phase in record_dict['phases']:
        
        phase_name = phase['name']
        
        for each in phase['measurements'].keys():
            
            
            template['phase_contents'].append({})
            template['phase_contents'][table_no]['name'] = phase_name
            if 'outcome' in phase['measurements'][each]:
                
                template['phase_contents'][table_no]['outcome'] = phase['measurements'][each]['outcome']
            if 'name' in phase['measurements'][each]:
                
                template['phase_contents'][table_no]['measure'] = phase['measurements'][each]['name']
            if 'measured_value' in phase['measurements'][each]:
                template['phase_contents'][table_no]['value'] = phase['measurements'][each]['measured_value']
            #if 'validators' in phase['measurements'][each]:
            #    template['phase_contents'][table_no]['validator'] = phase['measurements'][each]['validators'][0]
            table_no += 1
    

    names='PASS', 'FAIL','ERROR','ABORTED','TIMEOUT',
    size=[template['passed'],template['failed'],template['error'],template['aborted'],template['timeout']]
    
    
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    
    plt.pie(size,  colors=['green','red','blue','skyblue','orange'])
    plt.legend(names, loc="best")
    p=plt.gcf()
    
    p.gca().add_artist(my_circle)
    #plt.show()
    figname = template['dut_id'] + 'outcome.png'
    plt.savefig(figname)

    template_doc = DocxTemplate(template_file)
    img_size = Cm(7)  
    graph = InlineImage(template_doc, figname, img_size)
    template['graph'] = graph  
    file_string = str(template['dut_id'])+'_'+str(template['test_name'])+'_'+str(record_dict['start_time_millis']) +'_'+str(template['test_outcome'])+'.docx'
    
    
    target_file = Path(path) / file_string
    
    template_doc.render(template)
    template_doc.save(target_file)
    
    try:
        os.remove(figname)
    except:
        print('error removing', figname)
    
