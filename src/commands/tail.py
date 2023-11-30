import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input

def tail(args, out, virtual_input=None):
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
    if num_lines != 0:
        if file:
            with open(file) as f:
                lines = f.readlines()
                if len(lines) >= num_lines:
                    out += lines[-num_lines:]
                else:
                    out += lines
        elif virtual_input:
            virtual_input = flatten_virtual_input(virtual_input)
            if len(virtual_input) >= num_lines:
                out += virtual_input[-num_lines:]
            else:
                out += virtual_input
        else:
            lines = sys.stdin.readlines()
            if len(lines) >= num_lines:
                out += lines[-num_lines:]
            else:
                out += lines
    return out

def _tail(args, out, virtual_input=None):
    try:
        return tail(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out 