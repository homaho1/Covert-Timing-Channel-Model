import sys
import numpy as np
import random
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

def genSM(m):
    SM = []
    for i in range(m):
        SM.append(random.randrange(0,2))
    return SM

def genIPD(m, dist_type):
    IPD = [0]
    if dist_type == 0: #Expo
        for i in range(m):
            IPD.append(IPD[i] + np.random.exponential(1))
        return IPD
    else:
        for i in range(m):
            IPD.append(IPD[i] + np.random.uniform(0,1))
        return IPD

def get0(dist_type):
    if dist_type == 0: #Expo
        return random.uniform(0, 0.693147)
    else: #uni
        return random.uniform(0, 0.5)
    
def get1(dist_type):
    if dist_type == 0: #Expo
        return random.uniform(0.693147, 5)
    else: #uni
        return random.uniform(0.5, 1)
        

class buffer:
    def __init__(self, max_size, initial):
        self.max_size = max_size
        self.initial = initial
        self.current_size = 0
        
def stimulation(mode, m, init):
    B = 20
    SM = genSM(m)
#     print(SM)
    IPD = genIPD(2*(m+init), mode) #0 is expo 1 is uni
    buf = buffer(B, init)
    queue = []
    for i in range(init):
#         if len(IPD) == 0:
#             break
        queue.append(IPD.pop(0))
        buf.current_size += 1
#     print(queue)
#     print(IPD)
#     print(len(IPD))
    time = queue[buf.current_size-1]
#     print(time)
    # print(buf.current_size)
    queue.pop(0)
    buf.current_size -= 1
#     print(queue)
    for i in range(len(SM)):
        if SM[i] == 0:
            timeForNextSend = get0(mode)
        else:
            timeForNextSend = get1(mode)
#         print("Time interval " + str(timeForNextSend))

        beforetime = time + timeForNextSend
        while len(IPD) != 0 and beforetime >= IPD[0]:
            queue.append(IPD.pop(0))
            buf.current_size += 1
            if buf.current_size > buf.max_size:
#                 print("overflow with time " + str(time))
                return 1

        time = time + timeForNextSend
        if buf.current_size == 0:
#             print("underflow with time " + str(time))
            return 2
        
        queue.pop(0)
        buf.current_size -= 1    
#     print("none with time " + str(time))
    return 0

#step 1
num = [2,6,10,14,18]
expo_16 = []
for j in range(len(num)):
    over = 0
    under = 0
    none = 0
    
    for k in range(500):
        x = stimulation(0, 16, num[j])
        if x == 0:
            none += 1
        elif x == 1:
            over += 1
        else:
            under += 1
    expo_16.append(under/500)
    expo_16.append(over/500)
    expo_16.append(none/500)

# print(expo_16)
# print("\n")
expo_32 = []
for j in range(len(num)):
    over = 0
    under = 0
    none = 0
    
    for k in range(500):
        x = stimulation(0, 32, num[j])
        if x == 0:
            none += 1
        elif x == 1:
            over += 1
        else:
            under += 1
    expo_32.append(under/500)
    expo_32.append(over/500)
    expo_32.append(none/500)

# print(expo_32)
# print("\n")

#step 2
num = [2,6,10,14,18]
uni_16 = []
for j in range(len(num)):
    over = 0
    under = 0
    none = 0
    
    for k in range(500):
        x = stimulation(1, 16, num[j])
        if x == 0:
            none += 1
        elif x == 1:
            over += 1
        else:
            under += 1
    uni_16.append(under/500)
    uni_16.append(over/500)
    uni_16.append(none/500)

# print(uni_16)
# print("\n")

uni_32 = []
for j in range(len(num)):
    over = 0
    under = 0
    none = 0
    
    for k in range(500):
        x = stimulation(1, 32, num[j])
        if x == 0:
            none += 1
        elif x == 1:
            over += 1
        else:
            under += 1
    uni_32.append(under/500)
    uni_32.append(over/500)
    uni_32.append(none/500)

# print(uni_32)
# print("\n")

print("Source Distribution = Exponential")
table1 = [["M size", "i", "Underflow", "Overflow", "Success"],
         [16, 2, expo_16[0], expo_16[1], expo_16[2]],
         [16, 6, expo_16[3], expo_16[4], expo_16[5]],
         [16, 10, expo_16[6], expo_16[7], expo_16[8]],
         [16, 14, expo_16[9], expo_16[10], expo_16[11]],
         [16, 18, expo_16[12], expo_16[13], expo_16[14]],
         [32, 2, expo_32[0], expo_32[1], expo_32[2]],
         [32, 6, expo_32[3], expo_32[4], expo_32[5]],
         [32, 10, expo_32[6], expo_32[7], expo_32[8]],
         [32, 14, expo_32[9], expo_32[10], expo_32[11]],
         [32, 18, expo_32[12], expo_32[13], expo_32[14]],
        ]
print(tabulate(table1, headers='firstrow'))

print("\nSource Distribution = Uniform")
table2 = [["M size", "i", "Underflow", "Overflow", "Success"],
         [16, 2, uni_16[0], uni_16[1], uni_16[2]],
         [16, 6, uni_16[3], uni_16[4], uni_16[5]],
         [16, 10, uni_16[6], uni_16[7], uni_16[8]],
         [16, 14, uni_16[9], uni_16[10], uni_16[11]],
         [16, 18, uni_16[12], uni_16[13], uni_16[14]],
         [32, 2, uni_32[0], uni_32[1], uni_32[2]],
         [32, 6, uni_32[3], uni_32[4], uni_32[5]],
         [32, 10, uni_32[6], uni_32[7], uni_32[8]],
         [32, 14, uni_32[9], uni_32[10], uni_32[11]],
         [32, 18, uni_32[12], uni_32[13], uni_32[14]],
        ]
print(tabulate(table2, headers='firstrow'))
