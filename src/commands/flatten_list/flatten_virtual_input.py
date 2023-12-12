from collections import deque


def flatten_virtual_input(input_list):
    """
    Flatten a list of strings by separating into different lines.

    Parameters:
    - input_list (deque): List of strings to be flattened.

    Returns:
    - result (deque): A deque containing flattened strings
                      with preserved line breaks.
    """
    result = deque()
    for string in input_list:
        lines = string.split("\n")
        result.extend([line + "\n" for line in lines[:-1]])
        if lines[-1]:
            result.append(lines[-1])
    return result
