import sys
import os
from collections import deque
from lark_parser import Parser
from autocomplete import Autocomplete
from shell_lexer import ShellLexer
from prompt_toolkit.lexers import PygmentsLexer

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
from commands.wc import wc
from commands.unsafe import unsafe

parser = Parser()

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
    "cut": cut,
    "wc": wc
}


def eval_single(command, virtual_input=None):
    app = command[0]
    args = command[1:]
    out = deque()
    # Handles command substitution
    if app.startswith('`') and app.endswith('`'):
        app = list(eval(app[1:-1]))[-1].strip()
    for index, arg in enumerate(args):
        if arg.startswith('`') and arg.endswith('`'):
            args[index:index+1] = [x.strip() for x in list(eval(arg[1:-1]))]
    if app.startswith('_') and app[1:] in apps:
        out = unsafe(apps[app[1:]], args, out, virtual_input)
        return out
    elif app in apps:
        out = apps[app](args, out, virtual_input)
        return out
    else:
        raise ValueError(f"Unsupported application: {app}")


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
            else:
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
                this_command = []
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
            raise ValueError("Wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"Unexpected command line argument {sys.argv[1]}")
        out = eval(sys.argv[2])
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        autocomplete = Autocomplete(apps, os.getcwd())
        history = autocomplete.get_history()
        session = autocomplete.get_session()
        current_dir = os.getcwd()

        while True:
            if os.getcwd() != current_dir:
                current_dir = os.getcwd()
                autocomplete.update_autocomplete(current_dir)

            cmdline = session.prompt(f"{current_dir}> ",
                                     completer=autocomplete.get_completer(),
                                     complete_while_typing=False,
                                     lexer=PygmentsLexer(ShellLexer))
            history.append_string(cmdline)

            if cmdline.lower() == 'exit':
                break

            if not cmdline:
                # Empty command line
                continue

            out = eval(cmdline)
            while len(out) > 0:
                print(out.popleft(), end="")


if __name__ == "__main__":
    main()
