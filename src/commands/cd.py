import os


def cd(args, out, virtual_input=None):
    """
    Change the current working directory to the specified directory.

    Parameters:
    - args (list): A list containing the target directory path.
    - out (deque): Unused parameter,
                   included for consistency with other functions.
    - virtual_input (deque, optional): Unused parameter, included for
                                       consistency with other functions.

    Returns:
    - out (deque): The deque remains unchanged as
                   'cd' does not produce any output.

    Raises:
    - ValueError: If no directory is specified or
                  more than one directory is specified.
    - FileNotFoundError: If the directory specified in the argument
                         could not be found.
    """
    if len(args) == 0 or len(args) > 1:
        raise ValueError(
            f"Invalid command line arguments: cd {' '.join(args)}")
    os.chdir(args[0])
    return out
