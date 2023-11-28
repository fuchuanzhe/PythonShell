import os

def cd(args, out, virtual_input=None):
    if len(args) == 0 or len(args) > 1:
        raise ValueError("Wrong number of command line arguments")
    os.chdir(args[0])
    return out

def _cd(args, out, virtual_input=None):
    try:
        return cd(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out