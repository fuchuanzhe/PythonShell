import sys

def uniq(args, out):
    case_insensitive = False
    file = None

    if len(args) == 1 and args[0] == "-i":
        case_insensitive = True
    elif len(args) == 2 and args[0] == "-i":
        case_insensitive = True
        file = args[1]
    elif len(args) == 1:
        file = args[0]
    elif len(args) == 0:
        pass
    else:
        raise ValueError("Invalid command line arguments")

    return uniq_helper(out, file, case_insensitive)

def uniq_helper(out, file, case_insensitive):
    prev_line = None
    if file:
        with open(file) as f:
            for line in f:
                if len(out) > 0:
                    prev_line = out[-1].strip().lower() if case_insensitive else out[-1].strip()
                line_to_compare = line.strip().lower() if case_insensitive else line.strip()
                if line_to_compare != prev_line:
                    out.append(line.strip() + "\n")
    else:
        for line in sys.stdin:
            if not prev_line:
                prev_line = line.strip()
                continue
            prev_line = prev_line.lower() if case_insensitive else prev_line
            line_to_compare = line.strip().lower() if case_insensitive else line.strip()
            if line_to_compare != prev_line:
                print(prev_line)
            prev_line = line.strip()
        out.append(prev_line + "\n")
    return out

def _uniq(args, out):
    try:
        return uniq(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out
