from pwn import *
import zlib
import tempfile

context.arch = 'amd64'

# p = remote('localhost', 5000)
p = remote('cyberchallenge.disi.unitn.it', 8102)

p.recvuntil(b"Here is the file:\n")

compressed = p.recvline().strip()
compressed = bytes.fromhex(compressed.decode())
original_program = zlib.decompress(compressed)

with open('./file', 'wb') as f:
    f.write(original_program)
    f.close()
    program = ELF(f.name, checksec=False)


program.asm(0x1214, 'MOV DWORD PTR [rbp-0x4], 0x0')
program.asm(0x125f, 'XOR EAX, 0x0')
program.asm(0x1280, 'MOV RAX, 0x4060')

# program.asm(0x1287, 'MOV RDI, 0x4060')
# program.asm(0x1239, 'JMP 0x1269')
# program.asm(0x1287, 'MOV RDI, RDX')
# program.asm(offset, "mov rax, 0")





compressed = zlib.compress(program.data)
p.sendline(compressed.hex().encode())
print(p.recvall().decode())
