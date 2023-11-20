import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob
from parser import Parser

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



def eval(cmdline, out):
    parser = Parser()
    raw_commands = parser.parse(cmdline)
    for command in raw_commands:
        app = command[0]
        args = command[1:]
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
            out = deque()
            eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
