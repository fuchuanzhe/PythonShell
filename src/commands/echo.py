# does not work with "", ', ``
# will treat echo "hi" as two separate commands
# echo hi; echo helllo works

def echo(out, args):
    out.append(" ".join(args) + "\n")