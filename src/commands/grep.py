import re
import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input

def grep(args, out, virtual_input=None):
    """
    Search for lines matching a specified regular expression pattern in files or standard input.

    Parameters:
    - args (list): A list of command-line arguments specifying the search pattern and files. 
                   If no file is given, 'grep' reads from standand input.
    - out (deque): The deque to which the matching lines will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the matching lines.
    
    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
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
    elif virtual_input:
        virtual_input = flatten_virtual_input(virtual_input)
        for line in virtual_input:
            if re.search(pattern, line):
                out.append(line.strip() + "\n")
    else: 
        for line in sys.stdin:
            if re.search(pattern, line):
                print(line.strip())
    return out 

def _grep(args, out, virtual_input=None):
    """The unsafe version of grep"""
    try:
        return grep(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out