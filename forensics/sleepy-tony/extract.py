from PIL import Image
import sys
import os


def binary_to_text(binary):
    text = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))
    return text


def extract_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_message = ''

    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):
            binary_message += str(pixel[j] & 1)

    return binary_to_text(binary_message)




if __name__ == '__main__':
    input_path = sys.argv[1]
    print(extract_message(input_path))


