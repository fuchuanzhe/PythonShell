import sys
from commands.flatten_list.flatten_virtual_input import flatten_virtual_input


def wc(args, out, virtual_input=None):
    print(virtual_input)
    files = None
    flag = None
    if len(args) > 0 and '-' in args[0]:
        if args[0] not in ["-l", "-w", "-m"]:
            raise ValueError("Invalid command line arguments")
        flag = args[0]
        files = args[1:]
    elif len(args) > 0:
        files = args

    lines, words, bytes_counts = 0, 0, 0
    if files:
        for file_path in files:
            with open(file_path, 'r') as file:
                content = file.read()
                lines, words, bytes_counts = wc_helper(content, lines, words, bytes_counts)
    elif virtual_input:
        virtual_input = flatten_virtual_input(virtual_input)
        for content in virtual_input:
            lines, words, bytes_counts = wc_helper(content, lines, words, bytes_counts)
    else:
        input_lines = sys.stdin.readlines()
        for content in input_lines:
            lines, words, bytes_counts = wc_helper(content, lines, words, bytes_counts)

    if flag == "-l":
        out.append(f"{lines}\n")
    elif flag == "-w":
        out.append(f"{words}\n")
    elif flag == "-m":
        out.append(f"{bytes_counts}\n")
    else:
        out.append(f"{lines}\n")
        out.append(f"{words}\n")
        out.append(f"{bytes_counts}\n")

    return out


def wc_helper(content, lines, words, bytes_counts):
    content_line = content.count('\n')  # Counting lines
    content_word = len(content.split())  # Counting words
    content_bytes_count = len(content.encode('utf-8'))  # Counting bytes

    lines += content_line
    words += content_word
    bytes_counts += content_bytes_count

    return lines, words, bytes_counts


def _wc(args, out, virtual_input):
    try:
        return wc(args, out, virtual_input)
    except Exception as err:
        out.clear()
        print(err)
        return out
