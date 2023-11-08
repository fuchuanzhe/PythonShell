import sys
from commands.flags.r import r
from commands.flags.o import o
from commands.flags.n import n
from commands.flags.nr import nr

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

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            arr.append(line.strip())

        flags = {
            "-r": r,
            "-o": o,
            "-n": n,
            "-nr": nr
            # "-k": k, #to do?
            # "-c": c, #to do?
            # "-u": u, #to do?
            # "-M": m #to do?
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