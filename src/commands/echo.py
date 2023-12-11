def echo(args, out, virtual_input=None):
    """
    Print a formatted string.

    Parameters:
    - args (list): A list of strings to be printed.
    - out (deque): The deque to which the result will be appended.
    - virtual_input (deque, optional): A deque representing input received
                                       from piping or redirection.

    Returns:
    - out (deque): The updated output list after appending
                   the concatenated string.
    """
    out.append(" ".join(args) + "\n")
    return out
