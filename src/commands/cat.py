import sys

def cat(args, out, virtual_input=None):
    if len(args) == 0:
        # handles pipe input
        if virtual_input:
            for line in virtual_input:
                print(line.strip())
        else:
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
