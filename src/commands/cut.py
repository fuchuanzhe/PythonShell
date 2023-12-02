import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input

def cut(args, out, virtual_input=None):
    """
    Process lines and extracts bytes from a file or standard input based on specified options. 

    Parameters:
    - args (list): A list of command-line arguments, must contain options. If no file is given, 'cut' reads from standand input. 
    - out (deque): The deque to which the cut segments will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the cut segments.
    
    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    file = None
    if len(args) == 2 and args[0] == "-b": 
        options = args[1]
    elif len(args) == 3 and args[0] == "-b": 
        options = args[1]
        file = args[-1]
    else: 
        raise ValueError("Invalid command line arguments")

    if file: 
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                out.append(cut_helper(line, options) + "\n")
    elif virtual_input:
        virtual_input = flatten_virtual_input(virtual_input)
        for line in virtual_input:
            out.append(cut_helper(line, options) + "\n")
    else: 
        for line in sys.stdin:
            print(cut_helper(line, options))
    return out

def cut_helper(line, options_range):
    """
    A helper function for 'cut', extracts bytes from a line based on specified options.

    Parameters:
    - line (str): The input line to be processed.
    - options_range (str): The range of bytes to be extracted provided.

    Returns:
    - str: The formatted string after applying the cut based on the specified options.
    """
    segments = []
    options_range = merge(split_string_to_list(options_range))
    for option in options_range:
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

def split_string_to_list(options_range):
    """
    Split the input options string into a list of intervals.

    Parameters:
    - options_range (str): The ange of bytes to be extracted provided.

    Returns:
    - result (list): A list of intervals represented as lists.
    """
    result = []
    for option in options_range.split(','):
        if '-' in option:
            start, end = option.split('-')
            start = int(start) if start else float('-inf')
            end = int(end) if end else float('inf')
            result.append([start, end])
        else:
            result.append([int(option)])
    return result

def merge(intervals):
    """
    Merge overlapping intervals into non-overlapping intervals.

    Parameters:
    - intervals (list): A list of intervals, each interval is represented as a list, [a,b].

    Returns:
    - result (list): A list of merged intervals.
    """
    intervals = sorted(intervals, key=lambda x:x[0])
    result = []
    for i in intervals:
        newInterval = i
        if result:
            if len(result[-1]) == 1:
                if result[-1][0] >= i[0]:
                    newInterval = result.pop()
                    newInterval = i
            elif result[-1][1] >= i[0]: 
                newInterval = result.pop()
                if len(i) ==2 and i[1] > newInterval[1]:
                    newInterval[1] = i[1]      
        result.append(newInterval)
    return result

def _cut(args, out, virtual_input=None):
    """The unsafe version of cut"""
    try:
        return cut(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out