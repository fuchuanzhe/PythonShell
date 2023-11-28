import fnmatch
import os

def find(args, out, virtual_input=None):
    if len(args) == 2 and args[0] == "-name":
        dir = "."
    elif len(args) == 3 and args[1] == "-name":
        dir = args[0]
    else:
        raise ValueError("Invalid command line arguments")
    pattern = args[-1]
    
    def find_helper(current_path):
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                find_helper(item_path)
            elif fnmatch.fnmatch(item, pattern):
                out.append(item_path + "\n")

    find_helper(dir)
    return out  

def _find(args, out, virtual_input=None):    
    try:
        return find(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out