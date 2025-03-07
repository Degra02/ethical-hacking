import math
from Crypto.Util.number import long_to_bytes

n, e, c = open("message.txt").readlines()
n, e, c = int(n), int(e), int(c)

def int_cbrt(x: int):
    l, r = 0, x
    while l < r:
        mid = (l + r + 1) // 2
        if mid ** 3 <= x:
            l = mid
        else:
            r = mid - 1

    return l

m = math.floor(int_cbrt(c))
print(long_to_bytes(m))
