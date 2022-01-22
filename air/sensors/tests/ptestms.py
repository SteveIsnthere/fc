def controlInputRequired(current, current_v, target, timeToAlign, maxAuthority):
    #maxAuthority in acceleration

    diff = target - current

    accelerationNeeded = 2 * \
        (diff / timeToAlign ** 2 - current_v / timeToAlign)

    controlInput = accelerationNeeded / maxAuthority

    if controlInput >= 1:
        controlInput = 1
    elif controlInput <= -1:
        controlInput = -1

    return controlInput

import time
import numpy as np

loopCount = 0
startingTime = time.time()
endingTime = startingTime + 1

while True:
    loopCount += 1

    for _ in range(100):
        controlInputRequired(np.random.rand()*100, np.random.rand()*100, np.random.rand()*100, np.random.rand()*10, np.random.rand()*100)
    if time.time() >= endingTime:
        break


print(str(loopCount)+"loops")
