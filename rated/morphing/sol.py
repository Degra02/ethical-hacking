from pwn import disasm

def disassemble_and_xor(binary_string):
    modified_data = bytearray(binary_string)
    hex_values = []
    while True:
        instructions = list(disasm(binary_string).splitlines())
        cmp_found = False
        for i, line in enumerate(instructions):
            if 'cmp    al, 0x' in line: # instruction containing flag char
                next_instr = instructions[i + 1]
                if 'je ' in next_instr:
                    hex_value = int(line.split("al,")[1].strip(), 16)
                    if hex_value == 0x3c: continue
                    hex_values.append(hex(hex_value))
                    hex_string = ''.join(h[2:] for h in hex_values)
                    print(bytes.fromhex(hex_string).decode('utf-8', errors='ignore'))
                    modified_data = [(a ^ hex_value) for a in modified_data]
                    cmp_found = True
                    break

        if not cmp_found:
            break

        binary_string = bytes(modified_data)

    return binary_string, hex_values


binary_string = open('./mysec.bin', 'rb').read()
initial_bytes = bytes((a ^ 0x42) for a in binary_string)

_, flag = disassemble_and_xor(initial_bytes)
hex_string = ''.join(h[2:] for h in flag)
res = bytes.fromhex(hex_string).decode('utf-8', errors='ignore')


# UniTN{m0rph1ng_x0r}
