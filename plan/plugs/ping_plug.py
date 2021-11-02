from openhtf import plugs
from subprocess import check_output

class PingPlug(plugs.BasePlug):
    '''A Plug that performs basic network Ping.'''
    def __init__(self):
      print('Instantiating %s!' % type(self).__name__)
    def ping(self, host):
      result = True
      ping_command = ['ping','-c','4', host] 
      ping_output = check_output(ping_command)
      
      result = 'TTL expired' in str(ping_output)
      return not result


#TODO
    # Add support for presets, etc
       
    def tearDown(self):
      # This method is optional.  If implemented, it will be called at the end
      # of the test.
      print('Tearing down %s!' % type(self).__name__)
