from pygments.lexer import RegexLexer, include
from pygments.token import Comment, Operator, Keyword, String


class ShellLexer(RegexLexer):
    """
    Lexer for shell commands.

    This lexer is designed for syntax highlighting using Pygments.

    Attributes:
    - name (str): The name of the lexer ('ShellLexer').
    - tokens (dict): A dictionary defining the tokenization rules using regex.

    Token Types:
    - Keyword: Shell command keywords (e.g., 'cat', 'ls', 'echo').
    - Operator: Shell operators (e.g., '<', '>', '|', '`').
    - String.Double: Double-quoted strings.
    - String.Single: Single-quoted strings.
    - Comment: Command-line options preceded by a dash ('-').

    Colour and Formatting:
    - Keyword: The keyword is bolded and coloured in green.
    - Operator: The operator is coloured in grey.
    - String.Double: The text enclosed within double quotes is coloured in red.
    - String.Single: The text enclosed within single quotes is coloured in red.
    - Comment: The flag is in italic and coloured in greenish-grey.
    """
    name = 'ShellLexer'

    tokens = {
        'root': [
            include('basic'),
            include('data')
        ],
        'basic': [
            (r'\b_?(cat|cd|cut|echo|find|grep|head|ls|pwd|'
             r'sort|tail|uniq|wc|exit)',
             Keyword),
            (r'<|>|\||\`', Operator)
        ],
        'data': [
            (r'(?s)"(\\\\|\\.|[^"\\])*"', String.Double),
            (r"(?s)'(\\\\|\\.|[^'\\])*'", String.Single),
            (r'-[a-zA-Z]+', Comment)
        ],
    }
