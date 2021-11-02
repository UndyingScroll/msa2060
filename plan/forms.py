
from spintop_openhtf.util.markdown import markdown
from plan.SAN_Plan import plann

passvalue = markdown("""
<img src="%s" width="800px" />

#PASS

All tests have passed; unplug all cables and stamp the side of the chassis.

""" % plann.image_url('.//pass.png'))

failevalue = markdown("""
<img src="%s" width="800px" />

#FAIL

One or more tests have failed.

""" % plann.image_url('.//fail.png'))

helpvalue = markdown("""

##Connect both the Power Supply 1 and Power Supply 2 cables.
##Connect the Controller A RJ-45 Ethernet cable (4).
##Connect the Controller B RJ-45 Ethernet cable (4).
##Turn both the Power Supply 1 (1) and Power Supply 2 (1) switches ON.
##Click OKAY to continue
<img src="%s" width="800px" />
""" % plann.image_url('.//image002.jpg'))


DUT_FORM_LAYOUT = {
    'schema':{
        'title': "IOX-SAN-2U-CORE",
        'type': "object",
        'required': ["serialnumber"],
        'properties': {
            'serialnumber': {
                'type': "string", 
                'title': "Serial Number"
            },
            'ponumber': {
                'type': "string",
                'title': 'Purchase Order'
            },
            'customer': {
                'type' : "string",
                'title': 'Customer'
            },
            'drive':{
                'type': "string",
                'default': "IOX-SAN-2U-6TB",
                'title' : "Installed Drive Part Number"
            },
            'drive_qty': {
                'type': "string",
                'default': "12",
                'title' : "Quantity of Installed Drives"
            },
            'dropdown': {
                'type': "string", 
                'default': "A Stock",
                'title': "Device Under Test Stock"
            },
        }
    },
    'layout':[
        "serialnumber",
        'ponumber',
        'customer',
         {
            "key": "drive",
            "type": "select",
            "titleMap": [
                { "value": "IOX-SAN-2U-6TB", "name": "IOX-SAN-2U-6TB" },
                { "value": "IOX-SAN-2U-8TB", "name": "IOX-SAN-2U-8TB" },
                { "value": "IOX-SAN-2U-10TB", "name": "IOX-SAN-2U-10TB" },
                { "value": "IOX-SAN-2U-12TB", "name": "IOX-SAN-2U-12TB" },
                { "value": "IOX-SAN-2U-14TB", "name": "IOX-SAN-2U-14TB" },
                { "value": "IOX-SAN-2U-16TB", "name": "IOX-SAN-2U-16TB" },
                { "value": "IOX-SAN-2U-18TB", "name": "IOX-SAN-2U-18TB" },
                { "value": "IOX-SAN-2U-72TB", "name": "IOX-SAN-2U-72TB" },
                { "value": "IOX-SAN-2U-96TB", "name": "IOX-SAN-2U-96TB" },
                { "value": "IOX-SAN-2U-120TB", "name": "IOX-SAN-2U-120TB" },
                { "value": "IOX-SAN-2U-144TB", "name": "IOX-SAN-2U-144TB" },
                { "value": "IOX-SAN-2U-168TB", "name": "IOX-SAN-2U-168TB" },
                { "value": "IOX-SAN-2U-192TB", "name": "IOX-SAN-2U-192TB" },
                { "value": "IOX-SAN-2U-216TB", "name": "IOX-SAN-2U-216TB" }
                ]
        },
         {
            "key": "drive_qty",
            "type": "select",
            "titleMap": [
                { "value": "12", "name": "12" },
                { "value": "11", "name": "11" },
                { "value": "10", "name": "10" },
                { "value": "9", "name": "9" },
                { "value": "8", "name": "8" },
                { "value": "7", "name": "7" },
                { "value": "6", "name": "6" },
                { "value": "5", "name": "5" },
                { "value": "4", "name": "4" },
                { "value": "3", "name": "3" },
                { "value": "2", "name": "2" },
                { "value": "1", "name": "1" },
                { "value": "0", "name": "0" }
                
            ]
        },
        {
            "key": "dropdown",
            "type": "select",
            "titleMap": [
                { "value": "A Stock", "name": "A Stock" },
                { "value": "B Stock", "name": "B Stock" }
                
            ]
        }

    ]
}


FAIL_FORM_LAYOUT = {
    'schema':{
        'title': "IOX-SAN-2U-CORE",
        'type': "object",
        'properties': {
            },
        
    },
    'layout':[
        {
            "type": "help",
            "helpvalue": failevalue
        }
        
    ]
}


DONE_FORM_LAYOUT = {
    'schema':{
        'title': "IOX-SAN-2U-CORE",
        'type': "object",
        'properties': {
            },
        
    },
    'layout':[
        {
            "type": "help",
            "helpvalue": passvalue
        }
        
    ]
}

SETUP_FORM_LAYOUT = {
    'schema':{
        'title': "IOX-SAN-2U-CORE",
        'type': "object",
        'properties': {
            },
        
    },
    'layout':[
        {
            "type": "help",
            "helpvalue": helpvalue
        }
        
    ]
}
