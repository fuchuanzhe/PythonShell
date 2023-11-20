import sys

def head(args, out):
    file = None
    if len(args) == 0:
        num_lines = 10
    elif len(args) == 1:
        num_lines = 10
        file = args[0]
    elif len(args) == 2 and args[0] == "-n":
        num_lines = int(args[1])
    elif len(args) == 3:
        num_lines = int(args[1])
        file = args[2]
    else:
        raise ValueError("Invalid command line arguments")
    
    if file:
        with open(file) as f:
            lines = f.readlines()
            for i in range(0, min(len(lines), num_lines)):
                out.append(lines[i])
    else:
        for n in range(num_lines):
            line = sys.stdin.readline()
            print(line.strip())
    return out

def _head(args, out):
    try:
        return head(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out
