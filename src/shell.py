import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob
from larkParser import Parser

from commands.cd import cd, _cd
from commands.cat import cat, _cat
from commands.echo import echo, _echo
from commands.grep import grep
from commands.ls import ls, _ls
from commands.pwd import pwd, _pwd
from commands.head import head, _head
from commands.tail import tail, _tail
from commands.find import find, _find
from commands.sort import sort, _sort
from commands.uniq import uniq, _uniq
from commands.cut import cut, _cut

# from colorama import Fore, Style
# def deb(*args):
#     print(Fore.BLUE , *args)
#     print(Style.RESET_ALL)

parser = Parser()


def eval(cmdline, out):
    raw_commands = parser.parse(cmdline)
    for command in raw_commands:
        app = command[0]
        args = command[1:]
        # handles command substitution
        for index, arg in enumerate(args):
            if arg.startswith('`') and arg.endswith('`'):
                args[index] = list(eval(arg[1:-1], out))[-1]
                # deb(args[index])
                out.clear()
        apps = {
            "pwd": pwd,
            "_pwd": _pwd,
            "cd": cd,
            "_cd" : _cd,
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
            "sort": sort,
            "_sort": _sort,
            "find": find,
            "_find": _find,
            "uniq" : uniq,
            "_uniq": _uniq,
            "cut" : cut,
            "_cut": _cut
        }
        
        if app in apps:
            out = apps[app](args, out)
            return out
        else:
            raise ValueError(f"unsupported application {app}")


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        eval(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()

            if not cmdline:
                # empty command line
                continue

            out = deque()
            eval(cmdline, out)
            # print(out)
            while len(out) > 0:
                print(out.popleft(), end="")
            print()
