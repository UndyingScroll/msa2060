from ..SAN_Plan import plann
from ..plugs.GreetPlug import GreetPlug
from spintop_openhtf import TestPlan,  conf
import openhtf as htf

@plann.testcase('UUT Setup')
@plann.plug(greet=GreetPlug)
def user_setup(test, greet):
    
    greet.user_setup()

