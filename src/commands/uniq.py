import sys

def uniq(args, out, virtual_input=None):
    case_insensitive = False
    file = None

    if len(args) == 1 and args[0] == "-i":
        case_insensitive = True
    elif len(args) == 2 and args[0] == "-i": #covered by test
        case_insensitive = True
        file = args[1]
    elif len(args) == 1: #covered by test
        file = args[0]
    elif len(args) == 0:
        pass
    else: #covered by test
        raise ValueError("invalid command line arguments")

    return uniq_helper(out, file, case_insensitive, virtual_input)

def uniq_helper(out, file, case_insensitive, virtual_input):
    prev_line = None
    if file:
        with open(file) as f:
            for line in f:
                if len(out) > 0:
                    prev_line = out[-1].strip().lower() if case_insensitive else out[-1].strip()
                line_to_compare = line.strip().lower() if case_insensitive else line.strip()
                if line_to_compare != prev_line:
                    out.append(line.strip() + "\n")
    elif virtual_input:
        virtual_input = flatten_newlines(virtual_input)
        for line in virtual_input:
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

def _uniq(args, out, virtual_input=None):
    try:
        return uniq(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out

def flatten_newlines(input_list):
    result = []
    for string in input_list:
        lines = string.split("\n")
        result.extend([line + "\n" for line in lines[:-1]])
        if lines[-1]:
            result.append(lines[-1])
    return result