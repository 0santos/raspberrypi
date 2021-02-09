#!/usr/bin/env python
from http import HTTPStatus
import urllib.request
import urllib.parse
import http.cookiejar
import re
import argparse

class Gateway:

    def __init__(self, user, pwd):
        if not self.is_valid_number(user):
            raise ValueError("%d is not a valid phone number." % user)

        self.user = user
        self.pwd = pwd
        self.maxlength = 130

        self.host = 'http://www.cvmovel.cv'
        self.user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        self.cookie = http.cookiejar.MozillaCookieJar()
        
    def fetch(self, uri, params):
        """
        Fetch: return de http code and content from the server
        """
        post_data = urllib.parse.urlencode(params).encode()
        
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        try:
            request = urllib.request.Request("{0}{1}".format(self.host, uri), post_data, headers={ 'User-Agent' : self.user_agent })
            resp = opener.open(request)
        except Exception as e:
            print (e)
            return ""
        
        self.dump() #Only for debugging

        return (resp.read().decode(), resp.code)
        
    def dump(self):
        if self.cookie:
            for item in self.cookie:
                print ("%s=%s" % (item.name, item.value))

    def user_auth(self):
        """
        User authentication
        """
        params = { 'sso_username' : self.user, 'sso_password' : self.pwd, 'Submit' : 'Entrar' }
        uri = "/sites/all/themes/cvmovel/int/checklogin.php"

        res, code = self.fetch(uri, params)
        if res and res.find(str(self.user)) > -1:
            is_auth = True
        else:
            is_auth = False

        return (is_auth, code)

    def send_sms(self, numbers, message):
        """
        Send the sms message to a destination phone number
        """
        if not self.is_valid_number(numbers):
            raise ValueError("%d is not a valid phone number." % numbers)
        
        params = { 'numero' : numbers, 'freeSms' : self.is_valid_text(message), 'left' : self.maxlength }
        uri = "/envio-de-mensagens-escritas"

        auth, code = self.user_auth()
        if auth and HTTPStatus.OK == code:
            res, code = self.fetch(uri, params)
            if code and HTTPStatus.OK == code:
                self.extract_info(res)
        else:
            print ('Auth: %s, Something went wrong please try again' % auth)

    def extract_info(self, data):
        pattern = re.compile(r'<div\s+class=\"integrations\"><span>(.*?)</span></div>', flags = re.M)
        match = pattern.findall(data)
        print(match)
        #if len(matchs) > 0:
        #    for log in matchs:
        #        print (log)
    
    def is_valid_number(self, phone_number):
        pattern = re.compile(r'^((95|97|98|99|59|58)\d{5})$')
        if pattern.match(str(phone_number)):
            return True
        else:
            return False

    def is_valid_text(self, text):
        if len(text) > self.maxlength:
            text = text[0:self.maxlength]
            self.maxlength = 0
        else:
            self.maxlength = int(self.maxlength - len(text))
        
        return text
    
def main():
    print ('Welcome, Dude')

    parser = argparse.ArgumentParser(prog='Gateway', usage='%(prog)s [options] <USER> <PASSWORD> <NUMBER> <TEXT>', description='Send 200 free text messages per month with CVMovel')
    parser.add_argument('user', type=int, help='User for login if not current user')
    parser.add_argument('password', type=str, help='Password to use when connecting to server')
    parser.add_argument('number', type=int, help='Destination phone number')
    parser.add_argument('text', type=str, nargs='+', help='Text message to be send')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1')
    args = parser.parse_args()

    #print (args)
    user = args.user
    password = args.password
    number = args.number
    text = ' '.join(args.text)

    if len(str(user)) == 7 and password.strip():
        gateway = Gateway(user, password)
    
    if len(str(number)) == 7 and text.strip():
        gateway.send_sms(number, text)

if __name__ == "__main__":
    main()
