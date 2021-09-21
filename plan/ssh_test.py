
import paramiko
import time


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.100.250', port=22, username='user', password='imagine01')

channel = ssh.invoke_shell()
rootpass="imagine01"
su = 'su - \n'
commands = ['cd /home/root','pwd','./eeprom_test -r']
buff = []
    
if True:
    channel.send(su)
    time.sleep(.2)
    while not channel.recv_ready():
       
        time.sleep(.1)
    print(channel.recv(1024).decode('utf-8'))
    time.sleep(.1)
    channel.send("%s\n" % rootpass)
    while not channel.recv_ready():
        print("Authenticating...")
        time.sleep(.1)
    
    buff.append(channel.recv(1024))
    
    for each in commands:
        time.sleep(.2)
        channel.send("%s\n" % each)
        time.sleep(.1)
        while not channel.recv_ready():
                time.sleep(.1)
        buff.append(channel.recv(1024))
    
for each in buff:
    print(each.decode('utf-8'))
                      
