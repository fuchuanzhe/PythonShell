import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def head(args, out, virtual_input=None):
    """
    Display the first few lines of a file or standard input.

    Parameters:
    - args (list): A list of command-line arguments specifying the flag, the number of lines and file.
                   If no file is given, 'head' reads from standand input.
                   If no number of lines is given, 'head' displays the first 10 lines.
    - out (deque): The deque to which the displayed lines will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the displayed lines.

    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
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
        if virtual_input:
            virtual_input = flatten_virtual_input(virtual_input)
            for n in range(0, min(len(virtual_input), num_lines)):
                line = virtual_input[n]
                out.append(line.strip() + "\n")
        else:
            for n in range(num_lines):
                line = sys.stdin.readline()
                print(line.strip())
    return out


def _head(args, out, virtual_input=None):
    """The unsafe version of head"""
    try:
        return head(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
