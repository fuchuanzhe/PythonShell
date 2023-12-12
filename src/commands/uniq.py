import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def uniq(args, out, virtual_input=None):
    """
    Remove duplicate consecutive lines from a file or standard input.

    Parameters:
    - args (list): Command-line arguments specifying options and file.
                   If no file is given, 'uniq' reads from standand input.
                   Options: '-i' forcase-insensitive comparison.
    - out (deque): The deque to which the unique lines will be appended.
    - virtual_input (deque, optional): A deque representing input received
                                       from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the unique lines.

    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    case_insensitive = False
    file = None

    if len(args) == 1 and args[0] == "-i":
        case_insensitive = True
    elif len(args) == 2 and args[0] == "-i":
        case_insensitive = True
        file = args[1]
    elif len(args) == 1 and args[0][0] != "-":
        file = args[0]
    elif len(args) == 0:
        pass
    else:
        raise ValueError(
            f"Invalid command line arguments: uniq {' '.join(args)}")

    return uniq_helper(out, file, case_insensitive, virtual_input)


def uniq_helper(out, file, case_insensitive, virtual_input):
    """
    A helper function for removing duplicate consecutive lines.

    Parameters:
    - out (deque): The deque to which the unique lines will be appended.
    - file (str, optional): The file path to read lines from.
    - case_insensitive (bool): Whether the comparison is case-insensitive.
    - virtual_input (deque, optional): A deque representing input received
                                       from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the unique lines.

    Raises:
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    prev_line = None
    if file:
        with open(file) as f:
            out = remove_consecutive_dup(
                out, f, prev_line, case_insensitive)
    elif virtual_input:
        virtual_input = flatten_virtual_input(virtual_input)
        out = remove_consecutive_dup(
            out, virtual_input, prev_line, case_insensitive)
    else:
        for line in sys.stdin:
            if not prev_line:
                prev_line = line.strip()
                continue
            prev_line = prev_line.lower() if case_insensitive else prev_line
            line_to_compare = line.strip().lower() \
                if case_insensitive else line.strip()
            if line_to_compare != prev_line:
                print(prev_line)
            prev_line = line.strip()
        out.append(f"{prev_line}\n")
    return out


def remove_consecutive_dup(out, input_lines, prev_line, case_insensitive):
    """
    Process a sequence of input lines,
    filtering and appending unique lines to an output list.

    Parameters:
    - input_lines (iterable): Iterable containing lines to process.
    - out (deque): Deque to which unique lines will be appended.
    - case_insensitive (bool): If True, perform case-insensitive comparison.

    Returns:
    - out (deque): The updated deque after appending the unique lines.
    """
    for line in input_lines:
        if len(out) > 0:
            prev_line = out[-1].strip().lower() \
                if case_insensitive else out[-1].strip()
        line_to_compare = line.strip().lower() \
            if case_insensitive else line.strip()
        if line_to_compare != prev_line:
            out.append(f"{line.strip()}\n")
    return out
