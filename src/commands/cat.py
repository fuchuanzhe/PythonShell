import sys

def cat(args, out):
    if len(args) == 0:
        for line in sys.stdin:
            print(line.strip())  # .strip() to remove new line char
    else:
        for a in args:
            try:
                with open(a) as f:
                    out.append(f.read())
            except FileNotFoundError:
                out.append(f"Error: File '{a}' not found.")
            except Exception as e:
                out.append(f"Error: {e}")
    return out
