from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

iv = b'InitializationVe'
key = b'My_EncryptionKey'
cipher_text_hex = '1ebad98bebd5a0269e5ab370b24474658fa2c9f20a69bcfe2990e91e71183c550ca6bc715a5fbc128c0de7c7cbf659b168a4ee9de8ea41de833a7e7a6efecdb0'

cipher_text = binascii.unhexlify(cipher_text_hex.replace(' ', ''))

cipher = AES.new(key, AES.MODE_CBC, iv)

decrypted = unpad(cipher.decrypt(cipher_text), AES.block_size)

print(decrypted.decode('utf-8'))

