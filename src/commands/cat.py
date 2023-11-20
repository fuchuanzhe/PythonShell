import sys

def cat(args, out):
    if len(args) == 0:
        for line in sys.stdin:
            print(line.strip())
    else:
        for a in args:
            with open(a) as f:
                out.append(f.read())
        return out
    
def _cat(args, out):
    try:
        return cat(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out
