import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def tail(args, out, virtual_input=None):
    """
    Display the last few lines of a file or standard input.

    Parameters:
    - args (list): Command-line arguments specifying the flag,
                   the number of lines and file.
                   If no file is given, 'tail' reads from standand input.
                   The default number of lines is 10.
    - out (list): The list to which the displayed lines will be appended.
    - virtual_input (deque, optional): A deque representing input received
                                       from piping or redirection.

    Returns:
    - out (list): The updated list after appending the displayed lines.

    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    file = None
    if len(args) == 0:
        num_lines = 10
    elif len(args) == 1 and args[0][0] != "-":
        num_lines = 10
        file = args[0]
    elif len(args) == 2 and args[0] == "-n" and args[1].isnumeric():
        num_lines = int(args[1])
    elif len(args) == 3 and args[0] == "-n" and args[1].isnumeric():
        num_lines = int(args[1])
        file = args[2]
    else:
        raise ValueError(
            f"Invalid command line arguments: tail {' '.join(args)}")

    if num_lines != 0:
        if file:
            with open(file) as f:
                lines = f.readlines()
                if len(lines) >= num_lines:
                    out += lines[-num_lines:]
                else:
                    out += lines
        elif virtual_input:
            virtual_input = list(flatten_virtual_input(virtual_input))
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
