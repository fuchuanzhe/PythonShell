import os
from os import listdir

# do i need to handle file not found? line 14 kinda handles it
# ls .  and ls .. working correctly


def ls(args, out, virtual_input=None):
    if len(args) == 0:
        ls_dir = os.getcwd()
    elif len(args) > 1:
        raise ValueError("wrong number of command line arguments")
    else:
        ls_dir = args[0]
    for f in listdir(ls_dir):
        if not f.startswith("."):
            out.append(f + "\n")
    return out
