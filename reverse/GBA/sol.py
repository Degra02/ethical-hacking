
enc_flag = b'\xff\xc4\xc3\xfe\xe4\xd1\xcb\xcb\xcb\xcb\xf5\xde\xc2\xcf\xf5\xcd\xc5\xc5\xce\xf5\xc5\xc6\xce\xf5\xce\xcb\xd3\xd9\xd7'

flag = ''.join(chr(a ^ 0xaa) for a in enc_flag)
print(flag)


# local_2c = 0xfec3c4ff;
# uStack_28 = 0xcbcbd1e4;
# uStack_24 = 0xc2def5cb;
# local_20 = 0xc5cdf5cf;
# uStack_1c = 0xc5f5cec5;
# uStack_18 = 0xcef5cec6;
# local_14 = 0xd7d9d3cb;
