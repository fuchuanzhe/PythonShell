from lark import Lark, Tree, Token
from glob import glob

class Parser:
    def __init__(self):
        self.grammar = r"""
value: command
        | QUOTED_STRING
        | UNQUOTED_STRING
        | value value

command: UNQUOTED_STRING
        | command command

start: value

UNQUOTED_STRING: /[^"`\s']+/
BACKTICK_QUOTED_STRING: /`[^`]*`/
QUOTED_STRING: ESCAPED_STRING | SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING | BACKTICK_QUOTED_STRING
SINGLE_QUOTED_STRING: /'[^']*'/
DOUBLE_QUOTED_STRING: /"[^"]*"/

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

"""

        self.parser = Lark(self.grammar, start="start")
    
    def parse(self, command):
        tree = self.parser.parse(command)
        all_tokens = Parser.extract_strings(tree)

        # handle globbing
        for index, token in enumerate(all_tokens):
            # glob('*.txt')
            # ['requirements.txt']
            if glob(token):
                all_tokens[index] = glob(token)
        # flatten
        all_tokens=[elem for sublist in all_tokens for elem in (sublist if isinstance(sublist, list) else [sublist])]




        commands = []
        for index, token in enumerate(all_tokens):
            # create lists in commands,
            # when a token ends with semicolon, create new list
            if index == 0:
                commands.append([token.strip('"')])
            elif token[-1] == ';':
                # commands[-1].append(token[:-1])
                commands.append([])
            else:
                commands[-1].append(token.strip('"'))
        return commands


    @staticmethod
    def extract_strings(tree):
        if isinstance(tree, Token):
            if tree.type in ['UNQUOTED_STRING', 'QUOTED_STRING']:
                return [tree.value]
            else:
                return []
        elif isinstance(tree, Tree):
            strings = []
            for child in tree.children:
                strings.extend(Parser.extract_strings(child))
            return strings
        else:
            return []

if __name__ == "__main__":
    parser = Parser()
    print(parser.parse('echo "hi"'))
    print(parser.parse('echo "hi"; echo "hello"'))
    print(parser.parse('cat ../.*ignore'))