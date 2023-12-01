import unittest
from collections import deque
import os
from shell import eval
from unittest.mock import patch, MagicMock
from io import StringIO

class TestShell(unittest.TestCase):
    def setUp(self):
        self.original_path = os.getcwd()
        os.chdir("test")

    def tearDown(self):
        # Restore the original working directory after the test
        os.chdir(self.original_path)

    def test_cat(self):
        out = eval("cat ./catTest/cat1.txt ./catTest/cat2.txt")
        self.assertEqual(out.popleft(), "this is cat1.\n")
        self.assertEqual(out.popleft(), "this is cat2.\n")
        self.assertEqual(len(out), 0)

    def test__cat(self):
        out = eval("_cat ./catTest/cat3.txt")
        self.assertEqual(len(out), 0)

    def test_cat_virtualin(self):
        out = eval("cat < catTest/cat1.txt")
        self.assertEqual(out.popleft(), "this is cat1.\n")
        self.assertEqual(len(out), 0)

    @patch("sys.stdin", StringIO("hello\nhihi\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_cat_stdin(self, mock_stdout):
            eval("cat")            
            output = mock_stdout.getvalue()
            expected_output = "hello\nhihi\n"
            self.assertEqual(output, expected_output)

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

    def test_cut6(self):
        out = eval("echo abc | cut -b -1,2-")
        self.assertEqual(out.popleft(), "abc\n")
        self.assertEqual(len(out), 0)

    @patch("sys.stdin", StringIO("abc\ndef\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_cut_stdin(self, mock_stdout):
            eval("cut -b 1")            
            output = mock_stdout.getvalue()
            expected_output = "a\nd\n"
            self.assertEqual(output, expected_output)

    def test__cut(self):
        out = eval("_cut")
        self.assertEqual(len(out), 0) 
    
    def test_cut7(self):
        out = eval("echo 12345678901 | cut -b 2-4,6,9-")
        self.assertEqual(out.popleft(), "2346901\n")
        self.assertEqual(len(out), 0)

    def test_cut8(self):
        out = eval("echo 12345678901 | cut -b 2-5,4,7,9")
        self.assertEqual(out.popleft(), "234579\n")
        self.assertEqual(len(out), 0)

    def test_cut9(self):
        out = eval("echo 12345678901 | cut -b 1-3,-2,5-")
        self.assertEqual(out.popleft(), "1235678901\n")
        self.assertEqual(len(out), 0)

    def test_cut_repeated_single(self):
        out = eval("echo 1234 | cut -b 2,3,3")
        self.assertEqual(out.popleft(), "23\n")
        self.assertEqual(len(out), 0)

    def test_echo(self):
        out = eval("echo foo")
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    # def test_echoException(self): #cannot think of errors for echo 
    #     out = eval("_echo")
    #     self.assertEqual(len(out), 0)

    def test_find(self):
        out = eval("find . -name findTest.txt")
        self.assertEqual(out.popleft(), "./findTest.txt\n")
        self.assertEqual(len(out), 0)

    def test__find(self):
        out = eval("_find . -name findTest.txt")
        self.assertEqual(out.popleft(), "./findTest.txt\n")
        self.assertEqual(len(out), 0)

    def test_find_dir(self):
        out = eval("find ./findTest -name findTest1.txt")
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(len(out), 0)

    def test_find_glob(self):
        out = eval("find ./findTest -name '*.txt'")
        self.assertEqual(out.popleft(), "./findTest/findTest2.txt\n")
        self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
        self.assertEqual(len(out), 0)

    def test_find_current_dir(self):
        out = eval("find -name '*.txt'")
        expected_result = ['./catTest/catTestFolder/cat3.txt\n', './catTest/catTestFolder/cat4.txt\n', 
                           './catTest/cat1.txt\n', './catTest/cat2.txt\n', 
                           './grepTest.txt\n', './cutTest/cut1.txt\n', 
                           './grepTest/grepTest1.txt\n', './grepTest/grepTest2.txt\n', 
                           './sortTest.txt\n', './uniqTest.txt\n', 
                           './sortTest/sortTest1.txt\n', './sortTest/sortTest2.txt\n', 
                           './findTest.txt\n', './uniqTest/uniq1.txt\n', './uniqTest/uniq2.txt\n', 
                           './uniqTest/uniq3.txt\n', './test.txt\n', './headTest.txt\n', 
                           './file2.txt\n', './cutTest.txt\n', './sorted.txt\n', 
                           './file1.txt\n', './findTest/findTest2.txt\n', './findTest/findTest1.txt\n', 
                           './headTest/head1.txt\n', './headTest/head2.txt\n', './tailTest.txt\n', 
                           './tailTest/tail1.txt\n']
        
        self.assertEqual(sorted(list(out)), sorted(expected_result))

    def test_find_wrong_input(self):
        with self.assertRaises(ValueError):
            out = eval("find -name")
    
    def test__find_wrong_input(self):
        out = eval("_find")
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

    @patch("sys.stdin", StringIO("hello\nhihi\nEOFError"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_grep_oneCmdArguments(self, mock_stdout):
            eval("grep hihi")            
            output = mock_stdout.getvalue()
            expected_output = "hihi\n"
            self.assertEqual(output, expected_output)

    def test_grep5(self): 
        out = eval("echo hihihi | grep hihi")
        self.assertEqual(out.popleft(), "hihihi\n")
        self.assertEqual(len(out), 0)
    
    def test_grep6(self): 
        out = eval("echo hello | grep hihi")
        self.assertEqual(len(out), 0)

    def test__grep6(self): 
        out = eval("_grep")
        self.assertEqual(len(out), 0)

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

    def test_head3(self):
        with self.assertRaises(ValueError):
            out = eval("head -n 2 hello world")
    
    def test__head4(self):
        out = eval("_head -n 2 headTest .txt")
        self.assertEqual(len(out), 0)

    def test_head4(self):
        out = eval("head < ./headTest/head2.txt")
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

    @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\nEOFError"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_head5(self, mock_stdout):
            eval("head -n 2")         
            output = mock_stdout.getvalue()
            expected_output = "hello\nhihi\n"
            self.assertEqual(output, expected_output)
    
    def test_head6(self):
        out = eval("head -n 0 headTest.txt")
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
    
    def test__pwd(self):
        out = eval("_pwd hello")
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

    def test__sort(self):
        out = eval("_sort sortTest.txt")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort_wrong_input(self):
        with self.assertRaises(ValueError):
            out = eval("sort -i sortTest.txt")

    def test__sort_wrong_input(self):
        out = eval("_sort -i sortTest.txt")
        self.assertEqual(len(out), 0)

    def test_sort_dir(self):
        out = eval("sort ./sortTest/sortTest1.txt")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort_r(self):
        out = eval("sort -r sortTest.txt")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)

    def test_sort_o(self): 
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

    def test_sort_n(self):
        out = eval("sort -n ./sortTest/sortTest2.txt")
        self.assertEqual(out.popleft(), "1\n")
        self.assertEqual(out.popleft(), "2\n")
        self.assertEqual(out.popleft(), "3\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "5\n")
        self.assertEqual(len(out), 0)

    def test_sort_virtual_input(self):
        out = eval("sort < sortTest.txt")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(len(out), 0)

    def test_sort_virtual_input_r(self):
        out = eval("sort -r < sortTest.txt")
        self.assertEqual(out.popleft(), "hihi my name\n")
        self.assertEqual(out.popleft(), "hihi\n")
        self.assertEqual(out.popleft(), "c\n")
        self.assertEqual(out.popleft(), "b\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "HIHI\n")
        self.assertEqual(len(out), 0)


    @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_stdin(self, mock_stdout):
            out = eval("sort")         
            expected_output = "hello\nhello1\nhihi\nhihi1\n"
            self.assertEqual(''.join(list(out)), expected_output)

    @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_stdin_r(self, mock_stdout):
            out = eval("sort -r")         
            expected_output = "hihi1\nhihi\nhello1\nhello\n"
            self.assertEqual(''.join(list(out)), expected_output)


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
        out = eval("tail -n 23 tailTest.txt")
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
        self.assertEqual(out.popleft(), "h\n")
        self.assertEqual(out.popleft(), "i\n")
        self.assertEqual(out.popleft(), "j\n")
        self.assertEqual(len(out), 0)

    def test_tail3(self):
        out = eval("tail < ./tailTest/tail1.txt")
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
    
    def test_tail4(self):
        with self.assertRaises(ValueError):
            out = eval("tail -n 2 hello world")

    @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_tail5(self, mock_stdout):
            out = eval("tail -n 2")         
            expected_output = "hello1\nhihi1\n"
            self.assertEqual(''.join(list(out)), expected_output)
    
    def test__tail6(self):
        out = eval("_tail -n 2 headTest .txt")
        self.assertEqual(len(out), 0)

    def test_tail7(self):
        out = eval("tail -n 0 headTest.txt")
        self.assertEqual(len(out), 0)

    @patch("sys.stdin", StringIO("hello\nhihi\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_tail8(self, mock_stdout):
            out = eval("tail -n 4")         
            expected_output = "hello\nhihi\n"
            self.assertEqual(''.join(list(out)), expected_output)
    
    def test_tail9(self):
        out = eval("tail -n 20 < ./tailTest/tail1.txt")
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

    @patch("sys.stdin", StringIO("hello\nhihi\nEOFError"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_uniq4(self, mock_stdout):
            eval("uniq")         
            output = mock_stdout.getvalue()
            expected_output = "hello\nhihi\n"
            self.assertEqual(output, expected_output)

    def test_uniq5(self):
        with self.assertRaises(ValueError):
            out = eval("uniq -r hello world")

    def test_uniq6(self):
        out = eval("uniq < ./uniqTest/uniq2.txt")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "ORANGE\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "BANANA\n")
        self.assertEqual(len(out), 0)

    def test_uniq7(self):
        out = eval("_uniq -r hello world")
        self.assertEqual(len(out), 0)

    def test_uniq8(self):
        out = eval("uniq < ./uniqTest/uniq1.txt")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(len(out), 0)

    @patch("sys.stdin", StringIO("hello\nHIHI\nhihi\nhihi\nEOFError"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_uniq9(self, mock_stdout):
            eval("uniq -i")         
            output = mock_stdout.getvalue()
            expected_output = "hello\nhihi\n"
            self.assertEqual(output, expected_output)

    def test_shellfile(self):
        with self.assertRaises(ValueError):
            out = eval("hello")

    def test_command_substitution(self):
        out = eval("echo `echo hi`")
        self.assertEqual(out.popleft().strip(), "hi")
        self.assertEqual(len(out), 0)

    def test_cut_out_of_range(self):
        out = eval("echo 123 | cut -b 5")
        self.assertEqual(out.popleft().strip(), "")
        self.assertEqual(len(out), 0)