import sys
import os
from collections import deque
from lark_parser import Parser

from commands.cd import cd, _cd
from commands.cat import cat, _cat
from commands.echo import echo, _echo
from commands.grep import grep, _grep
from commands.ls import ls, _ls
from commands.pwd import pwd, _pwd
from commands.head import head, _head
from commands.tail import tail, _tail
from commands.find import find, _find
from commands.sort import sort, _sort
from commands.uniq import uniq, _uniq
from commands.cut import cut, _cut
from commands.wc import wc, _wc

parser = Parser()


def eval_single(command, virtual_input=None):
    app = command[0]
    args = command[1:]
    out = deque()
    # handles command substitution
    if app.startswith('`') and app.endswith('`'):
        app = list(eval(app[1:-1]))[-1].strip()
    for index, arg in enumerate(args):
        if arg.startswith('`') and arg.endswith('`'):
            args[index:index+1] = [x.strip() for x in list(eval(arg[1:-1]))]
    # print(f"app: {app}, args: {args}")
    apps = {
            "pwd": pwd,
            "_pwd": _pwd,
            "cd": cd,
            "_cd": _cd,
            "echo": echo,
            "_echo": _echo,
            "ls": ls,
            "_ls": _ls,
            "cat": cat,
            "_cat": _cat,
            "head": head,
            "_head": _head,
            "tail": tail,
            "_tail": _tail,
            "grep": grep,
            "_grep": _grep,
            "sort": sort,
            "_sort": _sort,
            "find": find,
            "_find": _find,
            "uniq": uniq,
            "_uniq": _uniq,
            "cut": cut,
            "_cut": _cut,
            "wc": wc,
            "_wc": _wc
        }

    if app in apps:
        out = apps[app](args, out, virtual_input)
        return out
    else:
        raise ValueError(f"unsupported application {app}")


class Command:
    def __init__(self, command_tokens):
        self.command_tokens = command_tokens

    def pop_first(self):
        return self.command_tokens.popleft()

    def peek_first(self):
        return self.command_tokens[0]

    def __len__(self):
        return len(self.command_tokens)


def eval(cmdline):
    # print("evaluating", cmdline)
    raw_commands = parser.parse(cmdline)
    out = deque()
    for command in raw_commands:
        comm = Command(deque(command))
        local_out = None
        virtual_input = None
        this_command = []
        if comm.peek_first() in ['>', '<']:
            # special case: when the first token is a redirection
            # < file.txt cat == cat < file.txt
            # > file.txt cat == cat > file.txt
            if comm.peek_first() == '>':
                comm.pop_first()
                filename = comm.pop_first()
                virtual_input = None
                this_command = []
            elif comm.peek_first() == '<':
                comm.pop_first()
                filename = comm.pop_first()
                with open(filename, 'r') as f:
                    virtual_input = deque(f.readlines())
                this_command = []
        while len(comm) > 0:
            if comm.peek_first() == '|':
                comm.pop_first()
                local_out = eval_single(this_command, virtual_input)
                virtual_input = local_out
                this_command = []
            elif comm.peek_first() == '>':
                comm.pop_first()
                filename = comm.pop_first()
                local_out = eval_single(this_command, virtual_input)
                with open(filename, 'w') as f:
                    while len(local_out) > 0:
                        f.write(local_out.popleft())
                virtual_input = None
                this_command = []
            elif comm.peek_first() == '<':
                comm.pop_first()
                filename = comm.pop_first()
                with open(filename, 'r') as f:
                    virtual_input = f.readlines()
                local_out = eval_single(this_command, virtual_input)
                virtual_input = local_out
            else:
                this_command.append(comm.pop_first())

        if len(this_command) > 0:
            out += eval_single(this_command, virtual_input)
        else:
            out += local_out
    return out


def main():
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = eval(sys.argv[2])
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()

            if cmdline.lower() == 'exit':
                break

            if not cmdline:
                # empty command line
                continue

            out = eval(cmdline)
            while len(out) > 0:
                print(out.popleft(), end="")


if __name__ == "__main__":
    main()
