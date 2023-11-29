import sys

def cut(args, out, virtual_input=None):
    file = None
    if len(args) == 2 and args[0] == "-b": #covered by test
        options = args[1]
    elif len(args) == 3 and args[0] == "-b": #covered by test
        options = args[1]
        file = args[-1]
    else: #covered by test
        raise ValueError("invalid command line arguments")

    if file: #covered by test
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                out.append(cut_helper(line, options) + "\n")
    elif virtual_input: #covered by test
        virtual_input = flatten_newlines(virtual_input)
        for line in virtual_input:
            out.append(cut_helper(line, options) + "\n")
    else: #covered by test
        for line in sys.stdin:
            print(cut_helper(line, options))
    return out

def cut_helper(line, options):
    segments = []
    options = merge(split_string_to_list(options))
    for option in options:
        if len(option) == 1:
            position = option[0] - 1
            if 0 <= position < len(line):
                segments.append(line[position].strip())
        else:
            start, end = option
            start = start - 1 if type(start) != float else 0
            end = end if type(end) != float else len(line)
            segments.append(line[start:end].strip())
    return (''.join(segments))

def split_string_to_list(options):
    res = []
    for option in options.split(','):
        if '-' in option:
            start, end = option.split('-')
            start = int(start) if start else float('-inf')
            end = int(end) if end else float('inf')
            res.append([start, end])
        else:
            res.append([int(option)])
    return res

def merge(intervals):
    intervals = sorted(intervals, key=lambda x:x[0])
    res = []
    for i in intervals:
        newInterval = i
        if res:
            if len(res[-1]) == 1:
                if res[-1][0] >= i[0]:
                    newInterval = res.pop()
                    newInterval = i
            elif res[-1][1] >= i[0]: 
                newInterval = res.pop()
                if len(i) ==2 and i[1] > newInterval[1]:
                    newInterval[1] = i[1]      
        res.append(newInterval)
    return res

def _cut(args, out, virtual_input=None): #covered by test
    try:
        return cut(args, out, virtual_input)
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