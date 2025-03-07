from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes
import sympy

with open('./message.txt', 'rb') as f:
    n = int(f.readline())
    e = int(f.readline())
    c = int(f.readline())


factors = sympy.factorint(n)
p = list(factors.keys())[0]
q = list(factors.keys())[1]

phi_n = (p - 1) * (q - 1)
d = pow(e, -1, phi_n)
m = pow(c, d, n)

print(long_to_bytes(m))
