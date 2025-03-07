
TAPE_SIZE = 134

tape_bytes = b'\xf6\xff\x27\x00\x72\x00\x87\x00\xe9\x00\x3b\x00\x52\x00\x6c\x00\x38\x00\xd9\x00\x97\x00\x8d\x00\xf6\x00\xd1\x00\xa5\x00\xee\x00\xa6\x00\xee\x00\xda\x00\xb6\x00\xd8\x00\x6a\x00\x21\x00\x3d\x00\x4e\x00\x5b\x00\x04\x00\x95\x00\xe1\x00\xc8\x00\x9d\x00\xf0\x00\x82\x00\xd0\x00\xb9\x00\x4d\x00\x03\x00\x51\x00\x36\x00\x20\x00\x7f\x00\x44\x00\x22\x00\xce\x00\xfe\x00\x00\x00\x72\x00\xac\x00\xf3\x00\xc1\x00\xb5\x00\xa5\x00\xed\x00\xb0\x00\x83\x00\xa9\x00\xf6\x00\x0b\x00\x4d\x00\xcc\x00\xa0\x00\xc3\x00\x82\x00\x1e\x00\x59\x00\x55\x00\x28\x00'

tape = list(tape_bytes)

tape_xor_bytes = b'\x1d\x46\x07\x05\x14\x00\x06\x61\x28\x00\x7a\x0a\x36\x39\x74\x1b\x00\x41\x3c\x07\x00\x20\x5d\x75\x20'

offset = 0xf
for i in range(0, 0x19):
    tape[offset] = tape[offset] ^ tape_xor_bytes[i]
    offset += 2

print(tape)


head = 0
state = 0
reg = 0

def turing_machine():
    global head, state, reg

    while 0 <= head < TAPE_SIZE:
        if state == 3:
            tape[head] = reg
            state = 0
            head += 1
        elif state < 4:
            if state == 2:
                if tape[head] == -1:
                    head -= 1
                else:
                    state = 3
                    head += 1
            elif state < 3:
                if state == 0:
                    if tape[head] < 0:
                        head += 1
                    else:
                        reg = tape[head]
                        tape[head] = 0xffff
                        state = 1
                        head += 1
                elif state == 1:
                    reg ^= tape[head]
                    tape[head] = 0xffff
                    state = 2
                    head -= 1

turing_machine()

print(len(tape), ': ', tape)

flag = ''.join(str(tape[i]) for i in range(1, len(tape), 2))

byte_array = bytearray()
for i in range(0, len(flag), 2):
    byte_value = int(flag[i:i+2])
    byte_array.append(byte_value)

decoded_string = byte_array.decode('utf-8', errors='ignore')
print(decoded_string)
