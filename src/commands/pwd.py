import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob

def pwd(out):
    out.append(os.getcwd() + "\n")
    return out
