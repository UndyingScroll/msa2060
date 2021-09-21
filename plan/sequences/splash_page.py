from ..SAN_Plan import plann
from ..plugs.GreetPlug import GreetPlug
from spintop_openhtf import TestPlan,  conf
import openhtf as htf
from openhtf import PhaseResult
from itertools import groupby

@plann.testcase('Test Complete')
@htf.measures(htf.Measurement('status'))
@plann.plug(greet=GreetPlug)
def complete(test, greet):
    result = []
    for each in test.test_record.phases:
        result.append(each.outcome.value)
    
    status = result.count(result[0]) == len(result)
    
    
    try:
        greet.done(status)
    except:
        pass
    test.measurements.status = status