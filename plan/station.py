
_station = {'customer':'None','PO_number':'None', 'enclosure':'IOX-SAN-2U-CORE','drive':'None','drive_qty':0}  
_drives = {}
_bom = {'disks':0,'disk_pn':'None','disk_capacity': 'None' }

ip_addr = '10.0.0.2' # IP address of the SAN under test Controller A. Should typically be 10.0.0.2
port = 22
username = 'imagine'
password = '2021Imagine_'
timeout = 5


class versions(object):
    def __init__(self):
        self.release = '1.0'
