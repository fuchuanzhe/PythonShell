import os


def pwd(args, out, virtual_input=None):
    """
    Print the current working directory.

    Parameters:
    - args (list): No arguments are expected as
                   'pwd' does not take any arguments.
    - out (deque): The deque to which the current working directory
                   will be appended.
    - virtual_input (deque, optional): Unused parameter, included for
                                       consistency with other functions.

    Returns:
    - out (deque): The updated deque after appending
                   the current working directory.

    Raises:
    - ValueError: If any arguments are given.
    """
    if len(args) > 0:
        raise ValueError(
            f"Invalid command line arguments: pwd {' '.join(args)}")
    out.append(f"{os.getcwd()}\n")
    return out
