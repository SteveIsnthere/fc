from sys import getsizeof
import numpy as np
dummy = []
for _ in range(1000):
    dummy.append(np.random.rand())

print(getsizeof(dummy))

dummy = np.array(dummy,dtype=np.float32)

print(getsizeof(dummy))
dummy = "adasafsfa"
print(getsizeof(dummy))

print("a")