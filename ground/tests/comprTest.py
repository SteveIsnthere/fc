import numpy as np
import cv2
import time
path = 'sample1.jpg'

def compressed_img(path,compressed_res_x):
    raw_rgb_data = cv2.imread(path)
    raw_grayscale_data = cv2.cvtColor(raw_rgb_data, cv2.COLOR_RGB2GRAY)

    orig_height = raw_grayscale_data.shape[0]
    orig_width = raw_grayscale_data.shape[1]

    if compressed_res_x>=orig_width:
        compressed_res_x = orig_width # fail safe
        
    compressed_res_y = int(compressed_res_x*orig_height/orig_width)

    height_step = orig_height/compressed_res_y
    width_step = orig_width/compressed_res_x

    row_num = 0
    col_num = 0
    row_acc = []
    result = []
    for block in range(compressed_res_x*compressed_res_y):
        if (block)%compressed_res_x == 0 and block != 0:
            row_num+=1
            col_num = 0
            result.append(np.array(row_acc,dtype=np.int16))
            row_acc = []
        row_acc.append(int(np.mean(raw_grayscale_data[int(height_step*row_num):int(height_step*(row_num+1)),int(col_num*width_step):int((col_num+1)*width_step)])))
        col_num+=1

    result.append(np.array(row_acc,dtype=np.int16)) #last row
    result = np.array(result,dtype=np.int16)

    return result


startingTime = time.time()

for _ in range(10):
    n = compressed_img(path,25)

print(time.time() - startingTime)