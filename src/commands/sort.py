import sys
import os
from commands.flags.r import r
from commands.flags.o import o
from commands.flags.n import n

def sort(args, out):
    if len(args) > 2:
        for line in sys.stdin:
            print(line.strip())

    file = ''
    flag = ''

    if len(args) == 1:
        file = args[0]
    else:
        file = args[1]
        flag = args[0]

    arr = []

    if file[0:2] == '*.':
        pattern = file
        files = os.listdir(os.getcwd())

        selected_files = [file for file in files if file.endswith(pattern[1:])]
        if selected_files:
            for file in selected_files:
                with open(file) as f:
                    lines = f.readlines()
                    for line in lines:
                        arr.append(line.strip())

            flags = {
                "-r": r,
                "-o": o,
                "-n": n,
                "-nr": r
            }

            if flag != '':
                if flag in flags:
                    out = flags[flag](args, out, arr)
                else:
                    raise ValueError(f"unsupported application {flag}")
            else:
                arr.sort()
                for a in arr:
                    out.append(a + "\n") 
    else:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                arr.append(line.strip())

            flags = {
                "-r": r,
                "-o": o,
                "-n": n,
                "-nr": r
            }

            if flag != '':
                if flag in flags:
                    out = flags[flag](args, out, arr)
                else:
                    raise ValueError(f"unsupported application {flag}")
            else:
                arr.sort()
                for a in arr:
                    out.append(a + "\n") 
    return out 