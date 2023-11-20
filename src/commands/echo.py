# does not work with "", ', ``
# will treat echo "hi" as two separate commands
# echo hi; echo helllo works


def echo(args, out):
    out.append(" ".join(args) + "\n")
    return out

def _echo(args, out):
    try:
        return echo(args, out)
    except Exception as err:
        out.clear()
        print(err)
        return out