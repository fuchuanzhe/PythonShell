from lark import Lark, Tree, Token
from glob import glob


class Parser:
    """
    A class that represents a parser for shell commands.

    Attributes:
        grammar (str): The grammar rules for parsing shell commands.
        parser (Lark): The Lark parser object.

    Methods:
        parse(command): Parses a shell command and returns a list of commands.
        extract_strings(tree): Extracts strings from a parse tree.
    """
    def __init__(self):
        self.grammar = r"""
value: command
        | QUOTED_STRING
        | UNQUOTED_STRING
        | REDIRECT_IN
        | REDIRECT_OUT
        | PIPE
        | value value

command: UNQUOTED_STRING
        | command command

start: value

UNQUOTED_STRING: /[^"`><|\s']+/
REDIRECT_OUT: ">"    // Define redirection output operator as a token
REDIRECT_IN: "<"     // Define redirection input operator as a token
PIPE: "|"            // Define pipe operator as a token
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
        """
        Parses a shell command and returns a list of commands.

        Args:
            command (str): The shell command to be parsed.

        Returns:
            list: A list of commands extracted from the shell command.
        """
        tree = self.parser.parse(command)
        all_tokens = Parser.extract_strings(tree)

        # handle globbing
        for index, token in enumerate(all_tokens):
            # glob('*.txt')
            # ['requirements.txt']
            if glob(token):
                all_tokens[index] = glob(token)
        # flatten
        all_tokens = [elem for sublist in all_tokens for elem in (sublist if isinstance(sublist, list) else [sublist])]

        def is_quoted(token):
            return token.startswith('"') and token.endswith('"') or token.startswith("'") and token.endswith("'")

        def is_substituted(token):
            return token.startswith('`') and token.endswith('`')

        def remove_quotes(token):
            if is_quoted(token):
                return token[1:-1]
            else:
                return token

        commands = []
        for index, token in enumerate(all_tokens):
            # create lists in commands,
            # when a token ends with semicolon, create new list
            if index == 0:
                commands.append([remove_quotes(token)])
            elif ';' in token and not is_quoted(token) and not is_substituted(token):
                semicolon_splited_tokens = token.split(';')
                # "hi;ls;pwd;echo" -> ["hi", "ls", "pwd", "echo"]
                # ";" -> ["", ""]
                for index_, semicolon_splited_token in enumerate(semicolon_splited_tokens):
                    if index_ == 0:
                        commands[-1].append(remove_quotes(semicolon_splited_token))
                    else:
                        commands.append([])

            else:
                commands[-1].append(remove_quotes(token))
        return commands

    @staticmethod
    def extract_strings(tree):
        """
        Extracts strings from a parse tree.

        Args:
            tree (Token or Tree): The parse tree to extract strings from.

        Returns:
            list: A list of strings extracted from the parse tree.
        """
        if isinstance(tree, Token):
            return [tree.value]
        elif isinstance(tree, Tree):
            strings = []
            for child in tree.children:
                strings.extend(Parser.extract_strings(child))
            return strings
