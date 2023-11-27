import sys
def head(args, out, virtual_input=None):
    if len(args) == 0:
        if virtual_input:
            for line in virtual_input:
                print(line)
        else:
            for line in sys.stdin:
                print(line.strip())
        return out
    if len(args) != 1 and len(args) != 3:
        raise ValueError(f"wrong number of command line arguments: {args}")
    if len(args) == 1:
        num_lines = 10
        file = args[0]
    if len(args) == 3:
        if args[0] != "-n":
            raise ValueError("wrong flags")
        else:
            num_lines = int(args[1])
            file = args[2]

    with open(file) as f:
        lines = f.readlines()
        for i in range(0, min(len(lines), num_lines)):
            out.append(lines[i])
    return out
