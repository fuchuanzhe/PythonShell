import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob

def grep(args, out):
    # if len(args) < 2:
    #     raise ValueError("wrong number of command line arguments")
    if len(args) < 2:
        for line in sys.stdin:
            print(line.strip())
    
    pattern = args[0]
    files = args[1:]
    for file in files:
        with open(file) as f:
          # handle case when there is no such filename
          try:
              lines = f.readlines()
              for line in lines:
                  if re.match(pattern, line):
                      if len(files) > 1:
                          out.append(f"{file}:{line.strip()}\n")
                      else:
                          out.append(line)
          except FileNotFoundError:
              raise FileNotFoundError("The specified file was not found.") 
    # handle case when word is not found 
    if len(out) == 0:
        out.append("word not found!")

    return out 