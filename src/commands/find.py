import fnmatch
import os

def find(args, out, virtual_input=None):
    """
    Recursively search for files in a specified directory and its sub-directories matching a given pattern.

    Parameters:
    - args (list): A list of arguments containing the directory, flag and pattern. 
                   If no directory is given, the current directory is used.
    - out (deque): The deque to which the matching files will be appended.
    - virtual_input: Unused parameter, included for consistency with other functions.

    Returns:
    - out (deque): The updated deque after appending the matching files.
    
    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the directory specified in the argument could not be found.
    """
    if len(args) == 2 and args[0] == "-name":
        dir = "."
    elif len(args) == 3 and args[1] == "-name":
        dir = args[0]
    else:
        raise ValueError("Invalid command line arguments")
    pattern = args[-1]
    
    def find_helper(current_path):
        # Recursively search for files matching the pattern
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                find_helper(item_path)
            elif fnmatch.fnmatch(item, pattern):
                out.append(item_path + "\n")

    find_helper(dir)
    return out  

def _find(args, out, virtual_input=None): 
    """The unsafe version of find"""   
    try:
        return find(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
