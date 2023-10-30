import os


def cd(args, out):
    if len(args) == 0 or len(args) > 1:
        raise ValueError("wrong number of command line arguments")
    os.chdir(args[0])
    return out
