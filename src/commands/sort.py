import sys
from commands.flags.r import r
from commands.flags.o import o
from commands.flags.n import n

def sort(args, out, virtual_input=None):
    flags = {
            "-r": r,
            "-o": o,
            "-n": n
            }
    flag = None
    file = None

    if len(args) == 2 and args[0] in flags.keys():
        flag = args[0]
        file = args[1]
    elif len(args) == 1 and args[0] in flags.keys():
        flag = args[0]
    elif len(args) == 1:
        file = args[0]
    elif len(args) == 0:
        pass
    else:
        raise ValueError("Invalid command line arguments")

    arr = []

    if file:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                arr.append(line.strip())
            if flag:
                out = flags[flag](args, out, arr)
            else:
                arr.sort()
                for a in arr:
                    out.append(a + "\n") 
    elif virtual_input:
        virtual_input = flatten_newlines(virtual_input)
        for line in virtual_input:
            arr.append(line.strip())
        if flag:
            out = flags[flag](args, out, arr)
        else:
            arr.sort()
            for a in arr:
                out.append(a + "\n")
    else:
        lines = sys.stdin.readlines()
        for line in lines:
            arr.append(line.strip())
        if flag:
            out = flags[flag](args, out, arr)
        else:
            arr.sort()
            for a in arr:
                out.append(a + "\n")

    return out 

def _sort(args, out, virtual_input=None):
    try:
        return sort(args, out, virtual_input)
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