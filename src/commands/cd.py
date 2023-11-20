import os

def cd(args, out):
    if len(args) == 0 or len(args) > 1:
        raise ValueError("Wrong number of command line arguments")
    os.chdir(args[0])
    return out

def _cd(args, out):
    try:
        return cd(args, out)
    except ValueError:
        out.clear()
        print("Wrong number of command line arguments")
        return out
    except FileNotFoundError:
        out.clear()
        print("No such file or directory: " + args[0])
        return out