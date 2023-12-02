import sys
from commands.flags.r import r
from commands.flags.o import o
from commands.flags.n import n
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input

def sort(args, out, virtual_input=None):
    """
    Sort lines of text from files or standard input.

    Parameters:
    - args (list): A list of command-line arguments specifying sorting options and files.
                   If no file is given, 'sort' reads from standand input.
                   Sotrting options: '-r' for sort in reverse order, '-o' for output to file 'sorted.txt', '-n' for numerical sort.
    - out (deque): The deque to which the sorted lines will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the sorted lines.
    
    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
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
        virtual_input = flatten_virtual_input(virtual_input)
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
    """The unsafe version of sort"""
    try:
        return sort(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out