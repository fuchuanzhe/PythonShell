import re
import sys
from glob import glob

def grep(args, out):
    files = None
    if len(args) >= 2:
        pattern = re.compile(args[0])
        files = args[1:]
    elif len(args) == 1:
        pattern = re.compile(args[0])
    else:
        raise ValueError("Invalid command line arguments")

    if files:
        for file in files:
            with open(file) as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(pattern, line):
                        if len(files) > 1:
                            out.append(f"{file}:{line.strip()}\n")
                        else:
                            out.append(line)
    else:
        for line in sys.stdin:
            if re.search(pattern, line):
                print(line.strip())

    return out 

def _grep(args, out):
    try:
        return grep(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out