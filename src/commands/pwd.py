import os

def pwd(args, out, virtual_input=None):
    """
    Print the current working directory.

    Parameters:
    - args (list): No arguments are expected as 'pwd' does not take any arguments.
    - out (deque): The deque to which the current working directory will be appended.
    - virtual_input (deque, optional): Unused parameter, included for consistency with other functions.

    Returns:
    - out (deque): The updated deque after appending the current working directory.
    
    Raises:
    - ValueError: If any arguments are given.
    """
    if len(args) > 0:
        raise ValueError("Invalid command line arguments")
    out.append(os.getcwd() + "\n")
    return out

def _pwd(args, out, virtual_input=None):
    """The unsafe version of pwd"""
    try:
        return pwd(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
