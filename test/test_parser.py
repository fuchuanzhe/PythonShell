import unittest
from lark_parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_pwd(self):
        self.assertEqual(self.parser.parse("pwd"), [["pwd"]])

    def test_parse_cd(self):
        self.assertEqual(self.parser.parse("cd .."), [["cd", ".."]])

    def test_parse_echo(self):
        self.assertEqual(self.parser.parse("echo hi"), [["echo", "hi"]])

    def test_parse_ls(self):
        self.assertEqual(self.parser.parse("ls"), [["ls"]])

    def test_parse_ls_single_arg(self):
        self.assertEqual(self.parser.parse("ls ./src"), [["ls", "./src"]])

    def test_parse_cat(self):
        self.assertEqual(self.parser.parse("cat file.txt"), [["cat", "file.txt"]])

    def test_parse_head(self):
        self.assertEqual(self.parser.parse("head -n 15 file.txt"), [["head", "-n", "15", "file.txt"]])

    def test_parse_tail(self):
        self.assertEqual(self.parser.parse("tail -n 15 file.txt"), [["tail", "-n", "15", "file.txt"]])

    def test_parse_grep(self):
        self.assertEqual(self.parser.parse("grep hello dir1/file1.txt dir1/file2.txt"), [["grep", "hello", "dir1/file1.txt", "dir1/file2.txt"]])

    def test_parse_cut(self):
        self.assertEqual(self.parser.parse("cut -b -3,5- ./src/file.txt"), [["cut", "-b", "-3,5-", "./src/file.txt"]])

    def test_parse_find(self):
        self.assertEqual(self.parser.parse("find . -name *.py"), [["find", ".", "-name", "*.py"]])

    def test_parse_uniq(self):
        self.assertEqual(self.parser.parse("uniq -i file.txt"), [["uniq", "-i", "file.txt"]])

    def test_parse_sort(self):
        self.assertEqual(self.parser.parse("sort -r file.txt"), [["sort", "-r", "file.txt"]])

    def test_parse_double_quotes(self):
        self.assertEqual(self.parser.parse("echo \"hi\""), [['echo', 'hi']])

    def test_parse_semicolon(self):
        self.assertEqual(self.parser.parse("echo hi; echo hello"), [['echo', 'hi'], ['echo', 'hello']])

    def test_parse_command_substitution(self):
        self.assertEqual(self.parser.parse("echo \"hi `echo hello`\""), [['echo', 'hi `echo hello`']])

    def test_parse_pipe(self):
        self.assertEqual(self.parser.parse("cat dir/text1.txt | grep hello"), [["cat", "dir/text1.txt", "|", "grep", "hello"]])

    def test_parse_output_redirection(self):
        self.assertEqual(self.parser.parse("echo hi > file.txt"), [["echo", "hi", ">", "file.txt"]])

    def test_parse_input_redirection(self):
        self.assertEqual(self.parser.parse("echo hi > file.txt"), [["echo", "hi", ">", "file.txt"]])

    def test_parse_semicolon_pipe(self):
        self.assertEqual(self.parser.parse("echo hi; cat dir/text1.txt | grep hello"), [['echo', 'hi'], ['cat', 'dir/text1.txt', '|', 'grep', 'hello']])
