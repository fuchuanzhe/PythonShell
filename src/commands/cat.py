import sys

def cat(args, out, virtual_input=None):
    if len(args) == 0:
        # handles pipe input
        if virtual_input: #covered by test
            for line in virtual_input:
                out.append(line.strip() + "\n")
        else:
            for line in sys.stdin:
                print(line.strip())  
    else: #covered by test
        for a in args:
            a = a.strip()
            with open(a) as f:
                out.append(f.read())
    return out

def _cat(args, out, virtual_input=None):
    try:
        return cat(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
