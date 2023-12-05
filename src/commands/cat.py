import sys


def cat(args, out, virtual_input=None):
    """
    Concatenate and print the contents of files or standard input.

    Parameters:
    - args (list): A list of file to be concatenated. If no file is given, 'cat' reads from standand input.
    - out (deque): The deque to which the concatenated content will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the concatenated content.

    Raises:
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    if len(args) == 0:
        if virtual_input:
            for line in virtual_input:
                out.append(line.strip() + "\n")
        else:
            for line in sys.stdin:
                print(line.strip())
    else:
        for a in args:
            a = a.strip()
            with open(a) as f:
                out.append(f.read())
    return out


def _cat(args, out, virtual_input=None):
    """The unsafe version of cat"""
    try:
        return cat(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
