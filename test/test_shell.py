import unittest
from src.shell import eval
from collections import deque
import os

# left with cd test to figure out
class TestShell(unittest.TestCase):
    def test_cat(self):
        out = deque()
        eval("cat ./catTest/cat1.txt ./catTest/cat2.txt", out)
        self.assertEqual(out.popleft(), "this is cat1.\n")
        self.assertEqual(out.popleft(), "this is cat2.\n")
        self.assertEqual(len(out), 0)

    def test_cd(self):
        out = deque()

        # Get the absolute path of the current working directory
        current_path = os.path.abspath(os.getcwd())
        eval("cd catTest", out)
        cd_path = os.path.abspath(os.getcwd())
        current_path = os.path.normpath(current_path)

        # Construct the expected path in a platform-independent way
        expected_path = os.path.join(current_path, "catTest")

        # Use os.path.normpath to normalize the paths and make them consistent
        expected_path = os.path.normpath(expected_path)
        cd_path = os.path.normpath(cd_path)

        self.assertEqual(cd_path, expected_path)
        self.assertEqual(len(out), 0)
        os.chdir(current_path)

    def test_echo(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_find(self):
        out = deque()
        eval("find . -name findTest.txt", out)
        self.assertEqual(out.popleft(), "./findTest.txt\n")
        self.assertEqual(len(out), 0)

    def test_find1(self):
        out = deque()
        eval("find ./findTest -name findTest1.txt", out)
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(len(out), 0)

    def test_find2(self):
        out = deque()
        eval("find ./findTest -name *.txt", out)
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(out.popleft(), "./findTest/findTest2.txt\n")
        self.assertEqual(len(out), 0)

    def test_grep(self):
        out = deque()
        eval("grep hihi grepTest.txt", out)
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_grep1(self):
        out = deque()
        eval("grep hihi ./grepTest/grepTest1.txt", out)
        self.assertEqual(out.popleft(), "hihi 1\n")
        self.assertEqual(out.popleft(), "hihi my name 1\n")
        self.assertEqual(len(out), 0)

    def test_grep2(self):
        out = deque()
        eval("grep hihi grepTest.txt ./grepTest/grepTest1.txt", out)
        self.assertEqual(out.popleft(), "grepTest.txt:hihi\n")
        self.assertEqual(out.popleft(), "grepTest.txt:hihi my name\n")
        self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi 1\n")
        self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi my name 1\n")
        self.assertEqual(len(out), 0)

    def test_head(self):
        out = deque()
        eval("head headTest.txt", out)
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "d\n")
        self.assertEqual(out.popleft(), "e\n")
        self.assertEqual(out.popleft(), "f\n")
        self.assertEqual(out.popleft(), "g\n")
        self.assertEqual(len(out), 0)

    def test_head1(self):
        out = deque()
        eval("head -n 2 headTest.txt", out)
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)

    def test_head2(self):
        out = deque()
        eval("head -n 4 headTest.txt", out)
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(len(out), 0)

    def test_ls(self):
        out = deque()
        eval("ls", out)
        self.assertEqual(out.popleft(), "test_parser.py\n")
        self.assertEqual(out.popleft(), "sortTest.txt\n")
        self.assertEqual(out.popleft(), "grepTest\n")
        self.assertEqual(out.popleft(), "sorted.txt\n")
        self.assertEqual(out.popleft(), "tailTest.txt\n")
        self.assertEqual(out.popleft(), "findTest.txt\n")
        self.assertEqual(out.popleft(), "test_shell2.py\n")
        self.assertEqual(out.popleft(), "sortTest\n")
        self.assertEqual(out.popleft(), "test_shell.py\n")
        self.assertEqual(out.popleft(), "grepTest.txt\n")
        self.assertEqual(out.popleft(), "findTest\n")
        self.assertEqual(out.popleft(), "headTest.txt\n")
        self.assertEqual(out.popleft(), "catTest\n")
        self.assertEqual(len(out), 0)

    def test_pwd(self):
        out = deque()
        eval("pwd", out)
        self.assertEqual(out.popleft(), "/Users/hoshuhan/Documents/UCL/Y2/COMP0010 Software Engineering/code/comp0010-shell-python-p20/test\n")
        self.assertEqual(len(out), 0)

    def test_sort(self):
        out = deque()
        eval("sort sortTest.txt", out)
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort1(self):
        out = deque()
        eval("sort ./sortTest/sortTest1.txt", out)
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort2(self):
        out = deque()
        eval("sort -r sortTest.txt", out)
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)
    def test_sort3(self): # to check how to check output.txt
        out = deque()
        eval("sort -o sortTest.txt", out)
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

        file_path = 'sorted.txt'
        with open(file_path, 'r') as file:
            fileContent = file.read()

        self.assertEqual(fileContent, "HIHI\na\nb\nc\nhihi\nhihi my name\n")

    def test_sort4(self):
        out = deque()
        eval("sort -n ./sortTest/sortTest2.txt", out)
        self.assertEqual(out.popleft(), "1\n")
        self.assertEqual(out.popleft(), "2\n")
        self.assertEqual(out.popleft(), "3\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "5\n")

        self.assertEqual(len(out), 0)

    def test_sort5(self):
        out = deque()
        eval("sort -nr ./sortTest/sortTest2.txt", out)
        self.assertEqual(out.popleft(), "5\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "3\n")
        self.assertEqual(out.popleft(), "2\n")
        self.assertEqual(out.popleft(), "1\n")
        self.assertEqual(len(out), 0)

    def test_tail(self):
        out = deque()
        eval("tail tailTest.txt", out)
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "d\n")
        self.assertEqual(out.popleft(), "e\n")
        self.assertEqual(out.popleft(), "f\n")
        self.assertEqual(out.popleft(), "g\n")
        self.assertEqual(out.popleft(), "h\n")
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)

    def test_tail1(self):
        out = deque()
        eval("tail -n 2 tailTest.txt", out)
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)

    def test_tail2(self):
        out = deque()
        eval("tail -n 4 tailTest.txt", out)
        self.assertEqual(out.popleft(), "g\n")
        self.assertEqual(out.popleft(), "h\n")
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)


if __name__ == "__main__":
    import sys
    unittest.main()
