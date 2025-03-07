import unicodedata
import random
import string

replacements = {}

def find_replacements():
    for original_c in string.printable:
        for code in range(0, 0xFFFF + 1):
            char = chr(code)
            normalized = unicodedata.normalize('NFKC', char)

            if normalized == original_c and char != original_c:
                replacements[original_c] = replacements.get(original_c) + [char] if replacements.get(original_c) else [char]


def chinesify(input_string):
    input_string = input_string.lower()

    for c in input_string:
        char_replacements = replacements.get(c)
        if char_replacements:
            replacement = random.choice(char_replacements)
            input_string = input_string.replace(c, replacement)

    return input_string



char_to_egypt = {}
egypt_to_char = {}

for char in string.printable:
    egyptian = chr(random.choice(range(0x13220, 0x1342F + 1)))
    char_to_egypt[char] = egyptian
    egypt_to_char[egyptian] = char


injection = "𓌐𓍹𓈾𓌉𓌖𓍹𓏛𓊇𓏚𓐘𓏚𓌅𓈼𓍹𓊼𓐘𓏚𓏚𓊌𓏛𓎰𓍧𓍹𓉦𓌦𓍌𓈥𓍹𓋍𓉭𓉦𓐖𓐂𓍇𓉦𓍷𓋍𓐖𓉭𓐦𓊇𓌞𓍚𓋹𓍇𓉦𓉞𓈼𓈾𓎷𓐘𓏚𓊼𓍹𓐉𓊇𓏚𓌦𓏚𓍹𓈼𓈾𓎷𓐘𓏚𓐦𓊼𓌅𓊇𓏚𓈥𓈾𓍹𓍊𓍹𓈭𓉦𓍷𓉦𓐥𓉦𓊇𓋹𓏛𓍧𓍹𓉦𓌉𓌖𓍹𓍚𓋹𓉛𓏛𓈼𓈾𓎷𓐘𓏚𓐦𓌉𓈾𓈥𓏚𓍧𓍹𓐘𓏿𓋿𓏚𓍹𓋙𓌅𓏿𓌅𓌅𓏿𓍌𓐃𓋙𓍧"


original_encoding = "".join([egypt_to_char[c] for c in injection])
print(original_encoding)



