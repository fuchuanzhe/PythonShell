import re
import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def grep(args, out, virtual_input=None):
    """
    Search for lines matching a regex pattern in files or standard input.

    Parameters:
    - args (list): Command-line arguments specifying the pattern and files.
                   If no file is given, 'grep' reads from standand input.
    - out (deque): The deque to which the matching lines will be appended.
    - virtual_input (deque, optional): A deque representing input received
                                       from piping or redirection.

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
        raise ValueError(
            f"Invalid command line arguments: grep {' '.join(args)}")

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
                out.append(f"{line.strip()}\n")
    else:
        for line in sys.stdin:
            if re.search(pattern, line):
                print(line.strip())
    return out
