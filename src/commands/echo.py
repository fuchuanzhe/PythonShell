# does not work with "", ', ``
# will treat echo "hi" as two separate commands
# echo hi; echo helllo works


def echo(args, out):
    args1 = []
    for a in args:
        a = a.strip('"').strip("'")
        args1.append(a)
    
    out.append(" ".join(args1) + "\n")
    return out
