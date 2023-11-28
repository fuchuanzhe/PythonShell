import re
import sys
from collections import deque

def grep(args, out, virtual_input=None):
    files = None
    if len(args) >= 2: #covered by test
        pattern = re.compile(args[0])
        files = args[1:]
    elif len(args) == 1: #covered by test
        pattern = re.compile(args[0])
    else: #covered by test
        raise ValueError("Invalid command line arguments")

    if files: #covered by test
        for file in files:
            with open(file) as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(pattern, line):
                        if len(files) > 1:
                            out.append(f"{file}:{line.strip()}\n")
                        else:
                            out.append(line)
    elif virtual_input:
        virtual_input = flatten_newlines(virtual_input)
        for line in virtual_input:
            if re.search(pattern, line):
                out.append(line.strip() + "\n")
    else: 
        for line in sys.stdin:
            if re.search(pattern, line):
                print(line.strip())

    return out 

def _grep(args, out, virtual_input=None):
    try:
        return grep(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
    
def flatten_newlines(input_list):
    result = []
    for string in input_list:
        lines = string.split("\n")
        result.extend([line + "\n" for line in lines[:-1]])
        if lines[-1]:
            result.append(lines[-1])
    return result