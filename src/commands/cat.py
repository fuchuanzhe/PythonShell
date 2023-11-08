import sys

def cat(args, out):
    if len(args) == 0:
        for line in sys.stdin:
            print(line.strip())  # .strip() to remove new line char
    else:
        for a in args:
            with open(a) as f:
                out.append(f.read())
    return out
