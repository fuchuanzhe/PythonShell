# does not work with "", ', ``
# will treat echo "hi" as two separate commands
# echo hi; echo helllo works


def echo(args, out, virtual_input=None):
    # print(args)
    out.append(" ".join(args) + "\n")
    return out
