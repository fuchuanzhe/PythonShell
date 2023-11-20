import sys

def tail(args, out):
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
            if len(lines) >= num_lines:
                out += lines[-num_lines:]
            else:
                out += lines
    else:
        lines = sys.stdin.readlines()
        if len(lines) >= num_lines:
            out += lines[-num_lines:]
        else:
            out += lines
    return out

def _tail(args, out):
    try:
        return tail(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out