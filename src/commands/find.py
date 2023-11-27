import re
import sys
import os
from collections import deque
from glob import glob


# find ./GFG -name sample.txt 
# find ./GFG -name *.txt 
# find . -name test.txt
def find(args, out, virtual_input=None):
    
    if len(args) < 3:
        if virtual_input:
            for line in virtual_input:
                print(line.strip())
        else:
            for line in sys.stdin:
                print(line.strip())

    dir = args[0]
    file = args[2]

    if '*' in file:
        for filename in os.listdir(dir):
            # print(filename + "1")
            if file[1:] == filename[-len(file[1:]):]:
                out.append(dir + "/" + filename + "\n")
    else:
        for filename in os.listdir(dir):
            # print(filename + " 2 ")
            if filename == file:
                # print(filename + " in ")
                out.append(dir + "/" + filename + "\n")
        
        
    return out 