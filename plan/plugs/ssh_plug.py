from openhtf import plugs

import paramiko
import time


class SSHPlug(plugs.BasePlug):
    '''A Plug that performs basic network Ping.'''
    def __init__(self):
        print('Instantiating %s!' % type(self).__name__)

    def conf(self, addr, username,password,timeout,port,commands,sudo,prompt =  ':~#', s_delay = 0.1):
        self.addr = addr
        self.username = username
        self.password = password
        self.timeout = timeout
        self.port = port
        self.commands = commands
        self.sudo = sudo
        self.prompt = prompt
        self.s_delay = s_delay

    def shell(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.addr, port=self.port, username=self.username, password=self.password, timeout = self.timeout)
        stdin, stdout, stderr = ssh.exec_command('ls')
        channel = ssh.invoke_shell()
        rootpass= self.sudo
        su = 'su - \n'
        commands = self.commands
        
        buff = []
        prompt = self.prompt
        delay = self.s_delay    

        channel.send(su)
        time.sleep(.2)
        while not channel.recv_ready():
       
            time.sleep(.1)
        self.logger.info(channel.recv(1024).decode('utf-8'))
        time.sleep(.1)
        channel.send("%s\n" % rootpass)
        while not channel.recv_ready():
            self.logger.info("Authenticating...")
            time.sleep(delay)
        data = channel.recv(1024).decode('utf-8')
        buff.append(data.rstrip())
        self.logger.info(data.rstrip())
    
        for each in commands:
            got_prompt = False               
            time.sleep(delay)
            time.sleep(delay)
            channel.send("%s\n" % each)
            time.sleep(delay)
            while not got_prompt:
                while not channel.recv_ready():
                    time.sleep(.1)
                data = channel.recv(1024).decode('utf-8')
                time.sleep(delay)
                buff.append(data.rstrip())
                self.logger.info(data.rstrip())
                if prompt in data:
                    got_prompt = True

        ssh.close()
        return buff


#TODO
    # Add support for presets, etc
       
    def tearDown(self):
      # This method is optional.  If implemented, it will be called at the end
      # of the test.
      print('Tearing down %s!' % type(self).__name__)
