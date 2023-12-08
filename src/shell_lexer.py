from pygments.lexer import RegexLexer, include
from pygments.token import Comment, Operator, Keyword, String


class ShellLexer(RegexLexer):
    """Lexer for shell commands"""
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
            (r'-[a-zA-Z]+', Comment),
        ],
    }