import os
from os import listdir

def ls(args, out, virtual_input=None):
    if len(args) == 0:
        ls_dir = os.getcwd()
    elif len(args) > 1:
        raise ValueError("Wrong number of command line arguments")
    else:
        ls_dir = args[0]
    for f in listdir(ls_dir):
        if not f.startswith("."):
            out.append(f + "\n")
    return out

def _ls(args, out, virtual_input=None):
    try:
        return ls(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
