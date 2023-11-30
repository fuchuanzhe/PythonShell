import os

def pwd(args, out, virtual_input=None):
    if len(args) > 0:
        raise ValueError("Too many command line arguments")
    out.append(os.getcwd() + "\n")
    return out

def _pwd(args, out, virtual_input=None):
    try:
        return pwd(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
