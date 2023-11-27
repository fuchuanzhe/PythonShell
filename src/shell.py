import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob
from larkParser import Parser

from commands.cd import cd
from commands.cat import cat
from commands.echo import echo
from commands.grep import grep
from commands.ls import ls
from commands.pwd import pwd
from commands.head import head
from commands.tail import tail
from commands.find import find
from commands.sort import sort
from commands.uniq import uniq
from commands.cut import cut

# from colorama import Fore, Style
# def deb(*args):
#     print(Fore.BLUE , *args)
#     print(Style.RESET_ALL)

parser = Parser()


def eval_single(command, virtual_input=None):
    app = command[0]
    args = command[1:]
    out = deque()
    # handles command substitution
    for index, arg in enumerate(args):
        if arg.startswith('`') and arg.endswith('`'):
            local_out = deque()
            args[index] = list(eval(arg[1:-1]))[-1]
            # deb(args[index])

    apps = {
        "pwd": pwd,
        "cd": cd,
        "echo": echo,
        "ls": ls,
        "cat": cat,
        "head": head,
        "tail": tail,
        "grep": grep,
        "sort": sort,
        "find": find,
        "uniq": uniq,
        "cut": cut
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

    def __str__(self):
        return str(self.command_tokens)

def eval(cmdline):
    raw_commands = parser.parse(cmdline)
    out = deque()
    for command in raw_commands:
        comm = Command(deque(command))
        local_out = None
        virtual_input = None
        this_command = []
        while len(comm) > 0:
            if comm.peek_first() not in ['|', '>', '<']:
                this_command.append(comm.pop_first())
            elif comm.peek_first() == '|':
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

        if len(this_command) > 0:
            out += eval_single(this_command, virtual_input)
        else:
            out += local_out
    return out


if __name__ == "__main__":
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

            if not cmdline:
                # empty command line
                continue

            out = eval(cmdline)
            while len(out) > 0:
                print(out.popleft(), end="")
                print()
