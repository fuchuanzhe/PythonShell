def echo(args, out, virtual_input=None):
    out.append(" ".join(args) + "\n")
    return out

def _echo(args, out,virtual_input=None):
    try:
        return echo(args, out, virtual_input)
    except Exception as err:
        out.clear()
        return out