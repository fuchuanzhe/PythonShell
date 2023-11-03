import sys

def cut(args, out):
    file = None
    if len(args) == 2 and args[0] == "-b":
        options = args[1]
    elif len(args) == 3 and args[0] == "-b":
        options = args[1]
        file = args[-1]
    else:
        raise ValueError("invalid command line arguments")

    if file:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                out.append(cut_helper(line, options) + "\n")
    else:
        for line in sys.stdin:
            print(cut_helper(line, options))
    return out

def cut_helper(line, options):
    segments = []
    for option in options.split(','):
        if '-' in option:
            start, end = option.split('-')
            start = int(start) - 1 if start else None
            end = int(end) if end else None
            segments.append(line[start:end].strip())
        else:
            position = int(option) - 1
            if 0 <= position < len(line):
                segments.append(line[position].strip())
    return (''.join(segments))