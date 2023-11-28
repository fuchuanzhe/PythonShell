import unittest
from collections import deque
import os
from shell import eval
from unittest.mock import patch
from io import StringIO

# left with cd test to figure out
class TestShell(unittest.TestCase):
    def setUp(self):
        self.original_path = os.getcwd()
        os.chdir("test")

    def tearDown(self):
        # Restore the original working directory after the test
        os.chdir(self.original_path)

    def test_cat(self):
        print(os.path.abspath(os.getcwd()))
        out = eval("cat ./catTest/cat1.txt ./catTest/cat2.txt")
        self.assertEqual(out.popleft(), "this is cat1.\n")
        self.assertEqual(out.popleft(), "this is cat2.\n")
        self.assertEqual(len(out), 0)

    def test_cd(self):
        # Get the absolute path of the current working directory
        current_path = os.path.abspath(os.getcwd())
        out = eval("cd catTest")
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

    def test_cd_wrongFile(self):

        # Get the absolute path of the current working directory
        current_path = os.path.abspath(os.getcwd())
        out = eval("_cd cat")

        self.assertEqual(len(out), 0)
        os.chdir(current_path)

    def test_cd_wrongCmdLines(self):

        # Get the absolute path of the current working directory
        current_path = os.path.abspath(os.getcwd())
        out = eval("_cd catTest hello")

        self.assertEqual(len(out), 0)
        os.chdir(current_path)

    def test_cut(self):
        out = eval("cut -b 1 ./cutTest/cut1.txt")
        self.assertEqual(out.popleft(), "h\n")
        self.assertEqual(out.popleft(), "H\n")
        self.assertEqual(out.popleft(), "h\n")
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

    def test_cut2(self):
        out = eval("cut -b 2-3 ./cutTest/cut1.txt")
        self.assertEqual(out.popleft(), "ih\n")
        self.assertEqual(out.popleft(), "IH\n")
        self.assertEqual(out.popleft(), "ih\n")
        self.assertEqual(out.popleft(), "aa\n")
        self.assertEqual(out.popleft(), "bb\n")
        self.assertEqual(out.popleft(), "cc\n")
        self.assertEqual(out.popleft(), "dd\n")
        self.assertEqual(out.popleft(), "ee\n")
        self.assertEqual(out.popleft(), "ff\n")
        self.assertEqual(out.popleft(), "gg\n")
        self.assertEqual(out.popleft(), "hh\n")
        self.assertEqual(out.popleft(), "ii\n")
        self.assertEqual(out.popleft(), "jj\n")
        self.assertEqual(len(out), 0)

    def test_cut3(self):
        out = eval("cut -b 2- ./cutTest/cut1.txt")
        self.assertEqual(out.popleft(), "ihi\n")
        self.assertEqual(out.popleft(), "IHI\n")
        self.assertEqual(out.popleft(), "ihi my name\n")
        self.assertEqual(out.popleft(), "aaaa\n")
        self.assertEqual(out.popleft(), "bbbb\n")
        self.assertEqual(out.popleft(), "cccc\n")
        self.assertEqual(out.popleft(), "dddd\n")
        self.assertEqual(out.popleft(), "eeee\n")
        self.assertEqual(out.popleft(), "ffff\n")
        self.assertEqual(out.popleft(), "gggg\n")
        self.assertEqual(out.popleft(), "hhhh\n")
        self.assertEqual(out.popleft(), "iiii\n")
        self.assertEqual(out.popleft(), "jjjj\n")
        self.assertEqual(len(out), 0)

    def test_cut4(self):
        out = eval("cut -b 2-,3- ./cutTest/cut1.txt")
        self.assertEqual(out.popleft(), "ihi\n")
        self.assertEqual(out.popleft(), "IHI\n")
        self.assertEqual(out.popleft(), "ihi my name\n")
        self.assertEqual(out.popleft(), "aaaa\n")
        self.assertEqual(out.popleft(), "bbbb\n")
        self.assertEqual(out.popleft(), "cccc\n")
        self.assertEqual(out.popleft(), "dddd\n")
        self.assertEqual(out.popleft(), "eeee\n")
        self.assertEqual(out.popleft(), "ffff\n")
        self.assertEqual(out.popleft(), "gggg\n")
        self.assertEqual(out.popleft(), "hhhh\n")
        self.assertEqual(out.popleft(), "iiii\n")
        self.assertEqual(out.popleft(), "jjjj\n")
        self.assertEqual(len(out), 0)

    def test_cut5(self):
        with self.assertRaises(ValueError):
            out = eval("cut")


#     # def test_cut5(self):
#     #     out = deque()
#     #     eval("echo abc | cut -b 1", out)
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_cut6(self):
#     #     out = deque()
#     #     eval("echo abc | cut -b -1, 2-", out)
#     #     self.assertEqual(out.popleft(), "abc\n")
#     #     self.assertEqual(len(out), 0)

    def test_echo(self):
        out = eval("echo foo")
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    # def test_echoException(self): #cannot think of errors for echo 
    #     out = eval("_echo \$10")
    #     print(out)
    #     self.assertEqual(len(out), 0)

    def test_find(self):
        out = eval("find . -name findTest.txt")
        self.assertEqual(out.popleft(), "./findTest.txt\n")
        self.assertEqual(len(out), 0)

    def test_find1(self):
        out = eval("find ./findTest -name findTest1.txt")
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(len(out), 0)

    def test_find2(self):
        out = eval("find ./findTest -name \"*.txt\"")
        self.assertEqual(out.popleft(), "./findTest/findTest2.txt\n")
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(len(out), 0)

    def test_grep(self):
        out = eval("grep hihi grepTest.txt")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_grep1(self):
        out = eval("grep hihi ./grepTest/grepTest1.txt")
        self.assertEqual(out.popleft(), "hihi 1\n")
        self.assertEqual(out.popleft(), "hihi my name 1\n")
        self.assertEqual(len(out), 0)

    def test_grep2(self):
        out = eval("grep hihi grepTest.txt ./grepTest/grepTest1.txt")
        self.assertEqual(out.popleft(), "grepTest.txt:hihi\n")
        self.assertEqual(out.popleft(), "grepTest.txt:hihi my name\n")
        self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi 1\n")
        self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi my name 1\n")
        self.assertEqual(len(out), 0)

    def test_grep_noCmdArguments(self):
        with self.assertRaises(ValueError):
            out = eval("grep")

    # @patch('builtins.print', side_effect=['hihi\n'])
    # def test_grep_oneCmdArguments(self, mock_input):
    #     with StringIO() as mock_stdout:
    #         with patch('sys.stdout', mock_input):
    #             eval("grep hihi")
            
    #         self.assertEqual(mock_stdout.getvalue(), "hihi\n")
    
    # @patch('builtins.print', side_effect=['hello\n'])
    # def test_grep_oneWrongCmdArguments(self, mock_input):
    #     with StringIO() as mock_stdout:
    #         with patch('sys.stdout', mock_input):
    #             eval("grep hihi")
            
    #         self.assertEqual(mock_stdout.getvalue(), "")
        

    def test_head(self):
        out = eval("head headTest.txt")
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
        out = eval("head -n 2 headTest.txt")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)

    def test_head2(self):
        out = eval("head -n 4 headTest.txt")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(len(out), 0)

    def test_ls(self):
        out = eval("ls")        
        self.assertEqual(out.popleft(), "catTest\n")
        self.assertEqual(out.popleft(), "grepTest.txt\n")
        self.assertEqual(out.popleft(), "cutTest\n")
        self.assertEqual(out.popleft(), "grepTest\n")
        self.assertEqual(out.popleft(), "sortTest.txt\n")
        self.assertEqual(out.popleft(), "uniqTest.txt\n")
        self.assertEqual(out.popleft(), "test_shell.py\n")
        self.assertEqual(out.popleft(), "sortTest\n")
        self.assertEqual(out.popleft(), "test_shell2.py\n")
        self.assertEqual(out.popleft(), "findTest.txt\n")
        self.assertEqual(out.popleft(), "uniqTest\n")
        self.assertEqual(out.popleft(), "test.txt\n")
        self.assertEqual(out.popleft(), "test_parser.py\n")
        self.assertEqual(out.popleft(), "headTest.txt\n")
        self.assertEqual(out.popleft(), "file2.txt\n")
        self.assertEqual(out.popleft(), "cutTest.txt\n")
        self.assertEqual(out.popleft(), "sorted.txt\n")
        self.assertEqual(out.popleft(), "file1.txt\n")
        self.assertEqual(out.popleft(), "findTest\n")
        self.assertEqual(out.popleft(), "headTest\n")
        self.assertEqual(out.popleft(), "tailTest.txt\n")
        self.assertEqual(out.popleft(), "tailTest\n")
        self.assertEqual(out.popleft(), "__pycache__\n")
        self.assertEqual(len(out), 0)

    def test_ls_twoArg(self):
        with self.assertRaises(ValueError):
            out = eval("ls hello world")  

    def test_ls_oneArg(self):
        out = eval("ls cutTest")
        self.assertEqual(out.popleft(), "cut1.txt\n")
        self.assertEqual(len(out), 0)     

    def test_ls_unsafe(self):
        out = eval("_ls hello")
        self.assertEqual(len(out), 0)       

    def test_pwd(self):
        out = eval("pwd")
        self.assertEqual(out.popleft(), os.getcwd()+ "\n")
        self.assertEqual(len(out), 0)

    def test_sort(self):
        out = eval("sort sortTest.txt")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort1(self):
        out = eval("sort ./sortTest/sortTest1.txt")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort2(self):
        out = eval("sort -r sortTest.txt")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)
    def test_sort3(self): # to check how to check output.txt
        out = eval("sort -o sortTest.txt")
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
        out = eval("sort -n ./sortTest/sortTest2.txt")
        self.assertEqual(out.popleft(), "1\n")
        self.assertEqual(out.popleft(), "2\n")
        self.assertEqual(out.popleft(), "3\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "5\n")

        self.assertEqual(len(out), 0)

    def test_sort5(self):
        out = eval("sort -nr ./sortTest/sortTest2.txt")
        self.assertEqual(out.popleft(), "5\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "3\n")
        self.assertEqual(out.popleft(), "2\n")
        self.assertEqual(out.popleft(), "1\n")
        self.assertEqual(len(out), 0)

    def test_tail(self):
        out = eval("tail tailTest.txt")
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
        out = eval("tail -n 2 tailTest.txt")
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)

    def test_tail2(self):
        out = eval("tail -n 4 tailTest.txt")
        self.assertEqual(out.popleft(), "g\n")
        self.assertEqual(out.popleft(), "h\n")
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)

    # def test_uniq(self):
    #     out = eval("uniq -i")
    #     self.assertEqual(out.popleft(), "apple\n")
    #     self.assertEqual(out.popleft(), "banana\n")
    #     self.assertEqual(out.popleft(), "orange\n")
    #     self.assertEqual(len(out), 0)
    
    def test_uniq1(self):
        out = eval("uniq -i uniqTest.txt")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(len(out), 0)
    
    def test_uniq2(self):
        out = eval("uniq uniqTest.txt")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "BANANA\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "ORANGE\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(len(out), 0)
    
    def test_uniq3(self):
        out = eval("uniq ./uniqTest/uniq2.txt")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "ORANGE\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "BANANA\n")
        self.assertEqual(len(out), 0)

    # def test_uniq4(self):
    #     out = eval("uniq")
    #     self.assertEqual(out.popleft(), "apple\n")
    #     self.assertEqual(out.popleft(), "banana\n")
    #     self.assertEqual(out.popleft(), "BANANA\n")
    #     self.assertEqual(out.popleft(), "orange\n")
    #     self.assertEqual(out.popleft(), "ORANGE\n")
    #     self.assertEqual(len(out), 0)

    def test_uniq5(self):
        with self.assertRaises(ValueError):
            out = eval("uniq -r hello world")

#     # def test_uniq2(self):
#     #     out = deque()
#     #     eval("uniq < ./uniqTest/uniq2.txt", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "BANANA\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(out.popleft(), "ORANGE\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_uniq3(self):
#     #     out = deque()
#     #     eval("sort ./uniqTest/uniq1.txt | uniq", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_uniq4(self):
#     #     out = deque()
#     #     eval("sort ./uniqTest/uniq1.txt | uniq", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_uniq5(self):
#     #     out = deque()
#     #     eval("sort -i ./uniqTest/uniq2.txt | uniq", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(len(out), 0)


if __name__ == "__main__":
    import sys
    unittest.main()
