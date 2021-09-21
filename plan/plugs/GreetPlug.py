import sys, os
from ..forms import DUT_FORM_LAYOUT, SETUP_FORM_LAYOUT, DONE_FORM_LAYOUT, FAIL_FORM_LAYOUT
from openhtf.plugs.user_input import UserInput


class GreetPlug(UserInput):
    def prompt_tester_information(self):
        self.__response = self.prompt_form(DUT_FORM_LAYOUT)
        return self.__response

    def done(self, status):
        if status == True:

            self.prompt_form(DONE_FORM_LAYOUT,  timeout_s=5)
        else:
            self.prompt_form(FAIL_FORM_LAYOUT)


    def user_setup(self):
        
        self.prompt_form(SETUP_FORM_LAYOUT)
       # self.prompt("Connect the Power Supply 1 and Power Supply 2 AC power cables.\n\n" + \ 
       #             "Connect the Controller A RJ-45 Ethernet cable.\n\n" + \
       #             "Connect the QSFP A and QSFP B cable.\n\n" + \
       #             "When all cables are connected turn on the front panel power switch.\n\n")

    def greet_tester(self):
        try:
            self.prompt('Hello {serialnumber} !'.format(**self.__response))
        except AttributeError:
            
            raise Exception("Cannot greet tester before prompt_information")
        if self.__response['done'] == True:
            
            raise SystemExit

