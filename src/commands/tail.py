def tail(args, out, virtual_input=None):
    if len(args) == 0:
        if virtual_input:
            print(virtual_input)
        else:
            while True:
                line = input()
                print(line)
        return out

    if len(args) != 1 and len(args) != 3:
        raise ValueError("wrong number of command line arguments")
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
        if len(lines) >= num_lines:
            out += lines[-num_lines:]
        else:
            out += lines
    return out
