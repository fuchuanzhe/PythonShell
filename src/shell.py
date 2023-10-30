import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob
from commands.cd import cd
from commands.cat import cat
from commands.echo import echo
from commands.grep import grep
from commands.ls import ls
from commands.pwd import pwd
from commands.head import head
from commands.tail import tail


def eval(cmdline, out):
    raw_commands = []
    for m in re.finditer("([^\"';]+|\"[^\"]*\"|'[^']*')", cmdline):
        if m.group(0):
            raw_commands.append(m.group(0))
    for command in raw_commands:
        tokens = []
        for m in re.finditer("[^\\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
            if m.group(1) or m.group(2):
                quoted = m.group(0)
                tokens.append(quoted[1:-1])
            else:
                globbing = glob(m.group(0))
                if globbing:
                    tokens.extend(globbing)
                else:
                    tokens.append(m.group(0))
        app = tokens[0]
        args = tokens[1:]
        if app == "pwd":
            newOut = pwd(out)
            out = newOut
            # out.append(os.getcwd() + "\n")
        elif app == "cd":
            out = cd(args, out)
        elif app == "echo":
            out.append(" ".join(args) + "\n")
        elif app == "ls":
            if len(args) == 0:
                ls_dir = os.getcwd()
            elif len(args) > 1:
                raise ValueError("wrong number of command line arguments")
            else:
                ls_dir = args[0]
            for f in listdir(ls_dir):
                if not f.startswith("."):
                    out.append(f + "\n")
        elif app == "cat":
            for a in args:
                with open(a) as f:
                    out.append(f.read())
        elif app == "head":
            out = head(args, out)
        elif app == "tail":
            out = tail(args, out)
        elif app == "grep":
            newOut = grep(args, out)
            out = newOut
            # if len(args) < 2:
            #     raise ValueError("wrong number of command line arguments")
            # pattern = args[0]
            # files = args[1:]
            # for file in files:
            #     with open(file) as f:
            #         lines = f.readlines()
            #         for line in lines:
            #             if re.match(pattern, line):
            #                 if len(files) > 1:
            #                     out.append(f"{file}:{line}")
            #                 else:
            #                     out.append(line)
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
