from openhtf import plugs
import sys, requests, json, hashlib

from requests.packages.urllib3.exceptions import InsecureRequestWarning


class MSA2060(plugs.BasePlug):
    def __init__(self):
        print('Instantiating %s!' % type(self).__name__)

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.ip = '10.0.0.2'
        self.username = 'manage'
        self.password = '!manage'
        self.passstring = 'manage_!manage'.encode('utf-8')
        self.sessionKey = ''
        self.headers = {}
        self.message = ''

    def login(self):
        result = False
        self.url='https://{i}'.format(i = self.ip)
        self.passtring = '{u}_{p}'.format(u = self.username, p = self.password).encode('utf-8')
        self.headers={'datatype':'json'}
        auth_string=hashlib.sha256(self.passtring).hexdigest()
        try:
            r=requests.get(self.url+'/api/login/'+auth_string,headers=self.headers,verify=False)
            if str(r.status_code) == '200':
                response=json.loads(r.content)
                self.sessionKey=response['status'][0]['response']
                self.message = self.sessionKey
                if 'Authentication Unsuccessful' in self.sessionKey:
                    result = False
                else:
                    self.headers = {'sessionKey':self.sessionKey,'datatype':'json', 'Cache-Control': 'no-cache'}
                    result = True
            else:
                self.message = r.status_code
                result = False
        except:
            self.message = 'no connection at ip address'
            result = False
        return result

    def get(self,name,key):
        result = False
        url = '{u}/api/show/{n}'.format(u = self.url,n = name)
        r = requests.get(url,headers=self.headers,verify=False)
        if str(r.status_code) == '200':

            content = r.content.decode(encoding = 'utf-8')
            load = json.loads(content)
            if key in load:
                result = True
                return {'result':result, 'text':load[key]}
            else:
                result = False
                return {'result':result, 'text':'{n} key not found'.format(n = key)}
        else:
            result = False
            return {'result': result, 'text':'html code {s}'.format(s = r.status_code)}
    
    def set(self,names):
        result = False
        
        url = '{u}/api'.format(u = self.url)
        for each in names:
            url = '{u}/{e}'.format(u = url, e = each)
        r = requests.get(url,headers=self.headers,verify=False)
        if str(r.status_code) == '200':

            content = r.content.decode(encoding = 'utf-8')
            load = json.loads(content)
            if 'status' in load:
                data = load['status'][0]
                if data['return-code'] == 0:
                    result = True
                    return {'result': result, 'text': data}
                else:
                    result = False
                    return {'result': result, 'text': data}
            else:
                result = False
                return {'result': result, 'text': content}
        else:
            result = False
            return {'result': result, 'text':'html code {s}'.format(r.status_code)}
