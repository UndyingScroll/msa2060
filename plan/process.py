from spintop_openhtf import TestPlan,  conf
import openhtf as htf
from openhtf import PhaseResult

def onfailskip(test):
    result = []
    for each in test.test_record.phases:
        result.append(each.outcome.value)
    
    status = result.count(result[0]) == len(result)
    return status
