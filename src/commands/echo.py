def echo(args, out, virtual_input=None):
    """
    Print a formatted string by joining the arguments with spaces and append it to the output.
    
    Parameters:
    - args (list): A list of strings to be printed.
    - out (deque): The deque to which the result will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated output list after appending the concatenated string.
    """
    out.append(" ".join(args) + "\n")
    return out

def _echo(args, out,virtual_input=None):
    """The unsafe version of echo"""
    try:
        return echo(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out