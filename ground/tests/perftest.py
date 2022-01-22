import numpy as np
import time
arr = np.random.rand(20,20)

def arr_mod(arr):
    number = np.random.rand()
    arr += number
    arr -= number
    arr *= number
    arr /= number
    return arr

count = 0
startingTime = time.time()
interval = 1
endingTime = startingTime + interval

while True:
    count += 1
    arr = arr_mod(arr)
    if time.time() >= endingTime:
        break

print("Score: {} (Base Score 10000: Apple M1)".format(int(count/309856*10000)))
