import sys
# requirement: if no file specified, should use stdin

def cat(out, args):
    if len(args) == 0:
        for line in sys.stdin:
            print(line.strip()) # .strip() to remove new line char
    else:
        for a in args:
            with open(a) as f:
                out.append(f.read())