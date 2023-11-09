from lark import Lark, Tree, Token

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

UNQUOTED_STRING: /[^\s"']+/
QUOTED_STRING: ESCAPED_STRING | SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING | BACKTICK_QUOTED_STRING
SINGLE_QUOTED_STRING: /'[^']*'/
DOUBLE_QUOTED_STRING: /"[^"]*"/
BACKTICK_QUOTED_STRING: /`[^`]*`/

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

"""

        self.parser = Lark(self.grammar, start="start")
    
    def parse(self, command):
        tree = self.parser.parse(command)
        print(tree)
        return Parser.extract_strings(tree)

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