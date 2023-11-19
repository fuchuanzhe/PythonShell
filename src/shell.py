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
