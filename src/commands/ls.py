import os
from os import listdir


def ls(args, out, virtual_input=None):
    """
    List the files and directories in a specified directory.

    Parameters:
    - args (list): Command-line arguments specifying the target directory.
                   If no directory is given, the current directory is used.
    - out (deque): The deque to which the files and directories
                   will be appended.
    - virtual_input (deque, optional): Unused parameter, included for
                                       consistency with other functions.

    Returns:
    - out (deque): The updated deque after appending the list of files and
                   directories.

    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the directory specified in the argument
                         could not be found.
    """
    if len(args) == 0:
        ls_dir = os.getcwd()
    elif len(args) > 1:
        raise ValueError(
            f"Invalid command line arguments: ls {' '.join(args)}")
    else:
        ls_dir = args[0]
    for f in listdir(ls_dir):
        if not f.startswith("."):
            out.append(f"{f}\n")
    return out
