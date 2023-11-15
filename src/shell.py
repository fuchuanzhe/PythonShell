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



def eval(cmdline, out):
    parser = Parser()
    raw_commands = parser.parse(cmdline)
    for command in raw_commands:
        app = command[0]
        args = command[1:]
        
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
