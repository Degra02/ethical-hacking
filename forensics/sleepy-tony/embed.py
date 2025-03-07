#!/usr/bin/env python3

from PIL import Image
import sys
import os


def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message


def embed_message(image_path, message, output_path):
    # Open the image
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Convert the message to binary
    binary_message = text_to_binary(message)

    # Embed the message into the image
    index = 0
    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):  # RGB channels
            if index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[index])
                index += 1
            else:
                pixel[j] = pixel[j] & ~1
        pixels[i] = tuple(pixel)

    # Create a new image with the modified pixels
    new_img = Image.new('RGB', img.size)
    new_img.putdata(pixels)
    new_img.save(output_path)

    print(f"Message embedded successfully in '{output_path}'")


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if os.path.exists('flag.txt'):
        with open('flag.txt', 'r') as file:
            flag = file.read()
    else:
        flag = 'UniTN{too_easy_to_be_true}'

    embed_message(input_path, flag, output_path)
