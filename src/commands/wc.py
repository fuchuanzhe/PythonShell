import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def wc(args, out, virtual_input=None):
    """
    Count lines, words, and byte counts in files or standard input.

    Parameters:
    - args (list): A list of command-line arguments specifying options and file.
                   If no file is given, 'wc' reads from standand input.
                   Options: '-l' outputs only the line count.
                            '-w' outputs only the word count.
                            '-m' outputs only the byte count.
    - out (deque): The deque to which the result will be appended.
    - virtual_input (deque, optional): A deque representing input received from piping or redirection.

    Returns:
    - out (deque): The updated deque after appending the unique lines.

    Raises:
    - ValueError: If the command-line arguments are invalid.
    - FileNotFoundError: If the file given in the arguments could not be found.
    """
    files = None
    flag = None
    if len(args) > 0 and '-' in args[0]:
        if args[0] not in ["-l", "-w", "-m"]:
            raise ValueError(f"Invalid command line arguments: wc {' '.join(args)}")
        flag = args[0]
        files = args[1:]
    elif len(args) > 0:
        files = args

    lines, words, bytes = 0, 0, 0
    if files:
        for file_path in files:
            with open(file_path, 'r') as file:
                content = file.read()
                lines, words, bytes = count_lines_words_bytes(content, lines, words, bytes)
    elif virtual_input:
        virtual_input = flatten_virtual_input(virtual_input)
        for content in virtual_input:
            lines, words, bytes = count_lines_words_bytes(content, lines, words, bytes)
    else:
        input_lines = sys.stdin.readlines()
        for content in input_lines:
            lines, words, bytes = count_lines_words_bytes(content, lines, words, bytes)

    if flag == "-l":
        out.append(f"{lines}\n")
    elif flag == "-w":
        out.append(f"{words}\n")
    elif flag == "-m":
        out.append(f"{bytes}\n")
    else:
        out.append(f"{lines}\n")
        out.append(f"{words}\n")
        out.append(f"{bytes}\n")
    return out


def count_lines_words_bytes(content, lines, words, bytes):
    """
    Count lines, words, and bytes in the given content.

    Parameters:
    - content (str): Input content to analyze.
    - lines (int): Current count of lines.
    - words (int): Current count of words.
    - bytes_counts (int): Current count of bytes.

    Returns:
    - tuple: Tuple containing updated counts for lines, words, and bytes.
    """
    content_line = content.count('\n')
    content_word = len(content.split())
    content_bytes = len(content.encode('utf-8'))

    lines += content_line
    words += content_word
    bytes += content_bytes

    return lines, words, bytes
