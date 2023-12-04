from collections import deque


def flatten_virtual_input(input_list):
    result = deque()
    for string in input_list:
        lines = string.split("\n")
        result.extend([line + "\n" for line in lines[:-1]])
        if lines[-1]:
            result.append(lines[-1])
    return result
