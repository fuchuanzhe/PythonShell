# import unittest
# from collections import deque
# import os
# from shell import eval

# class TestShell(unittest.TestCase):
#     def setUp(self):
#         self.original_path = os.getcwd()
#         # os.chdir("test")

#     def tearDown(self):
#         # Restore the original working directory after the test
#         os.chdir(self.original_path)

#     def test_cat(self):
#         print(os.path.abspath(os.getcwd()))
#         out = eval("cat ./catTest/cat1.txt ./catTest/cat2.txt")
#         self.assertEqual(out.popleft(), "this is cat1.\n")
#         self.assertEqual(out.popleft(), "this is cat2.\n")
#         self.assertEqual(len(out), 0)

#     # def test_cat_stdin(self):
#     #     out = deque()
#     #     print(os.path.abspath(os.getcwd()))
#     #     eval("cat < catTest/cat1.txt", out)
#     #     self.assertEqual(out.popleft(), "this is cat1.\n")
#     #     self.assertEqual(len(out), 0)

#     def test_cd(self):
#         # Get the absolute path of the current working directory
#         current_path = os.path.abspath(os.getcwd())
#         out = eval("cd catTest")
#         cd_path = os.path.abspath(os.getcwd())
#         current_path = os.path.normpath(current_path)

#         # Construct the expected path in a platform-independent way
#         expected_path = os.path.join(current_path, "catTest")

#         # Use os.path.normpath to normalize the paths and make them consistent
#         expected_path = os.path.normpath(expected_path)
#         cd_path = os.path.normpath(cd_path)

#         self.assertEqual(cd_path, expected_path)
#         self.assertEqual(len(out), 0)
#         os.chdir(current_path)

#     def test_cd_wrongFile(self):
#         out = deque()

#         # Get the absolute path of the current working directory
#         current_path = os.path.abspath(os.getcwd())
#         eval("_cd cat", out)

#         self.assertEqual(len(out), 0)
#         os.chdir(current_path)

#     def test_cd_wrongCmdLines(self):
#         out = deque()

#         # Get the absolute path of the current working directory
#         current_path = os.path.abspath(os.getcwd())
#         eval("_cd catTest hello", out)

#         self.assertEqual(len(out), 0)
#         os.chdir(current_path)

#     def test_echo(self):
#         out = eval("echo foo")
#         self.assertEqual(out.popleft(), "foo\n")
#         self.assertEqual(len(out), 0)

#     def test_find(self):
#         out = eval("find . -name findTest.txt")
#         self.assertEqual(out.popleft(), "./findTest.txt\n")
#         self.assertEqual(len(out), 0)

#     def test_find1(self):
#         out = eval("find ./findTest -name findTest1.txt")
#         self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
#         self.assertEqual(len(out), 0)

#     # def test_find2(self):
#     #     out = deque()
#     #     eval("find ./findTest -name *.txt", out)
#     #     self.assertEqual(out.popleft(), "./findTest/findTest2.txt\n")
#     #     self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_find3(self): #toconfirm
#     #     out = deque()
#     #     eval("find -name '*.txt'", out)
#     #     self.assertEqual(out.popleft(), "./findTest/findTest2.txt\n")
#     #     self.assertEqual(out.popleft(), "./findTest/findTest1.txt\n")
#     #     self.assertEqual(len(out), 0)

#     def test_grep(self):
#         out = eval("grep hihi grepTest.txt")
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "hihi my name\n")
#         self.assertEqual(len(out), 0)

#     def test_grep1(self):
#         out = eval("grep hihi ./grepTest/grepTest1.txt")
#         self.assertEqual(out.popleft(), "hihi 1\n")
#         self.assertEqual(out.popleft(), "hihi my name 1\n")
#         self.assertEqual(len(out), 0)

#     def test_grep2(self):
#         out = eval("grep hihi grepTest.txt ./grepTest/grepTest1.txt")
#         self.assertEqual(out.popleft(), "grepTest.txt:hihi\n")
#         self.assertEqual(out.popleft(), "grepTest.txt:hihi my name\n")
#         self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi 1\n")
#         self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi my name 1\n")
#         self.assertEqual(len(out), 0)

#     def test_grep3(self):
#         out = deque()
#         eval("grep d grepTest.txt", out)
#         self.assertEqual(len(out), 0)
    
#     # def test_grep4(self): #todo
#     #     out = deque()
#     #     eval("grep 'A..' grepTest/grep1.txt", out)
#     #     self.assertEqual(out.popleft(), "grepTest.txt:hihi\n")
#     #     self.assertEqual(out.popleft(), "grepTest.txt:hihi my name\n")
#     #     self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi 1\n")
#     #     self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi my name 1\n")
#     #     self.assertEqual(len(out), 0)
    
#     # def test_grep5(self): #todo
#     #     out = deque()
#     #     eval("cat grepTest/grep1.txt grepTest/grep2.txt | grep '...'", out)
#     #     self.assertEqual(out.popleft(), "grepTest.txt:hihi\n")
#     #     self.assertEqual(out.popleft(), "grepTest.txt:hihi my name\n")
#     #     self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi 1\n")
#     #     self.assertEqual(out.popleft(), "./grepTest/grepTest1.txt:hihi my name 1\n")
#     #     self.assertEqual(len(out), 0)



#     def test_head(self):
#         out = eval("head headTest.txt")
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "HIHI\n")
#         self.assertEqual(out.popleft(), "hihi my name\n")
#         self.assertEqual(out.popleft(), "a\n")
#         self.assertEqual(out.popleft(), "b\n")
#         self.assertEqual(out.popleft(), "c\n")
#         self.assertEqual(out.popleft(), "d\n")
#         self.assertEqual(out.popleft(), "e\n")
#         self.assertEqual(out.popleft(), "f\n")
#         self.assertEqual(out.popleft(), "g\n")
#         self.assertEqual(len(out), 0)

#     def test_head1(self):
#         out = eval("head -n 2 headTest.txt")
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "HIHI\n")
#         self.assertEqual(len(out), 0)

#     def test_head2(self):
#         out = eval("head -n 4 headTest.txt")
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "HIHI\n")
#         self.assertEqual(out.popleft(), "hihi my name\n")
#         self.assertEqual(out.popleft(), "a\n")
#         self.assertEqual(len(out), 0)

#     # def test_head3(self):
#     #     out = deque()
#     #     eval("head -n 50 headTest.txt", out)
#     #     self.assertEqual(out.popleft(), "hihi\n")
#     #     self.assertEqual(out.popleft(), "HIHI\n")
#     #     self.assertEqual(out.popleft(), "hihi my name\n")
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(out.popleft(), "b\n")
#     #     self.assertEqual(out.popleft(), "c\n")
#     #     self.assertEqual(out.popleft(), "d\n")
#     #     self.assertEqual(out.popleft(), "e\n")
#     #     self.assertEqual(out.popleft(), "f\n")
#     #     self.assertEqual(out.popleft(), "g\n")
#     #     self.assertEqual(out.popleft(), "h\n")
#     #     self.assertEqual(out.popleft(), "i\n")
#     #     self.assertEqual(out.popleft(), "j\n")
#     #     self.assertEqual(len(out), 0)
    
#     def test_head4(self):
#         out = deque()
#         eval("head -n 0 headTest.txt", out)
#         self.assertEqual(len(out), 0)
    
#     def test_head5(self):
#         out = deque()
#         eval("head ./headTest/head1.txt", out)
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "HIHI\n")
#         self.assertEqual(out.popleft(), "hihi my name\n")
#         self.assertEqual(len(out), 0)

#     # def test_head6(self):
#     #     out = deque()
#     #     eval("head < ./headTest/head1.txt", out)
#     #     self.assertEqual(out.popleft(), "hihi\n")
#     #     self.assertEqual(out.popleft(), "HIHI\n")
#     #     self.assertEqual(out.popleft(), "hihi my name\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_ls(self):
#     #     out = deque()
#     #     eval("ls", out)
        
#     #     self.assertEqual(out.popleft(), "catTest\n")
#     #     self.assertEqual(out.popleft(), "grepTest.txt\n")
#     #     self.assertEqual(out.popleft(), "grepTest\n")
#     #     self.assertEqual(out.popleft(), "sortTest.txt\n")
#     #     self.assertEqual(out.popleft(), "test_shell.py\n")
#     #     self.assertEqual(out.popleft(), "sortTest\n")
#     #     self.assertEqual(out.popleft(), "findTest.txt\n")
#     #     self.assertEqual(out.popleft(), "test_parser.py\n")
#     #     self.assertEqual(out.popleft(), "headTest.txt\n")
#     #     self.assertEqual(out.popleft(), "sorted.txt\n")
#     #     self.assertEqual(out.popleft(), "findTest\n")
#     #     self.assertEqual(out.popleft(), "tailTest.txt\n")
#     #     self.assertEqual(out.popleft(), "__pycache__\n")        
#     #     self.assertEqual(len(out), 0)

#     # def test_ls_dir(self):
#     #     out = deque()
#     #     eval("ls catTest", out)

#     #     self.assertEqual(out.popleft(), "cat1.txt\n")
#     #     self.assertEqual(out.popleft(), "cat2.txt\n")
#     #     self.assertEqual(len(out), 0)

#     def test_ls_dir_hidden(self):
#         out = deque()
#         eval("ls catTest/catTestFolder", out)
        
#         self.assertEqual(out.popleft(), "cat3.txt\n")
#         self.assertEqual(out.popleft(), "cat4.txt\n")
#         self.assertEqual(len(out), 0)

#     def test_pwd(self):
#         out = eval("pwd")
#         self.assertEqual(out.popleft(), os.getcwd()+ "\n")
#         self.assertEqual(len(out), 0)
    
#     # def test_cd_pwd(self):
#     #     out = deque()
#     #     eval(" cd catTest; pwd", out)
#     #     self.assertEqual(out.popleft(), os.getcwd()+ "\n")
#     #     self.assertEqual(len(out), 0)

    # def test_sort(self):
    #     out = eval("sort sortTest.txt")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

    # def test__sort(self):
    #     out = eval("_sort sortTest.txt")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

    # def test_sort_wrong_input(self):
    #     with self.assertRaises(ValueError):
    #         out = eval("sort -i sortTest.txt")

    # def test__sort_wrong_input(self):
    #     out = eval("_sort -i sortTest.txt")
    #     self.assertEqual(len(out), 0)

    # def test_sort_dir(self):
    #     out = eval("sort ./sortTest/sortTest1.txt")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

    # def test_sort_r(self):
    #     out = eval("sort -r sortTest.txt")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(len(out), 0)

    # def test_sort_o(self): 
    #     out = eval("sort -o sortTest.txt")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

    #     file_path = 'sorted.txt'
    #     with open(file_path, 'r') as file:
    #         fileContent = file.read()

    #     self.assertEqual(fileContent, "HIHI\na\nb\nc\nhihi\nhihi my name\n")

    # def test_sort_n(self):
    #     out = eval("sort -n ./sortTest/sortTest2.txt")
    #     self.assertEqual(out.popleft(), "1\n")
    #     self.assertEqual(out.popleft(), "2\n")
    #     self.assertEqual(out.popleft(), "3\n")
    #     self.assertEqual(out.popleft(), "4\n")
    #     self.assertEqual(out.popleft(), "5\n")
    #     self.assertEqual(len(out), 0)

    # def test_sort_virtual_input(self):
    #     out = eval("sort < sortTest.txt")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

    # def test_sort_virtual_input_r(self):
    #     out = eval("sort -r < sortTest.txt")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(len(out), 0)


    # @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\nEOFError"))
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_sort_stdin(self, mock_stdout):
    #         eval("sort")         
    #         output = mock_stdout.getvalue()
    #         expected_output = "hello\nhello1\nhihi\nhihi1\n"
    #         self.assertEqual(output, expected_output)

    # @patch("sys.stdin", StringIO("hello\nhihi\nhello1\nhihi1\nEOFError"))
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_sort_stdin_r(self, mock_stdout):
    #         eval("sort -r")         
    #         output = mock_stdout.getvalue()
    #         expected_output = "hihi1\nhihi\nhello1\nhello\n"
    #         self.assertEqual(output, expected_output)

    # def test_sort6(self):
    #     out = deque()
    #     eval("sort < ./sortTest/sortTest1.txt", out)
    #     self.assertEqual(out.popleft(), "HIHI\n")
    #     self.assertEqual(out.popleft(), "a\n")
    #     self.assertEqual(out.popleft(), "b\n")
    #     self.assertEqual(out.popleft(), "c\n")
    #     self.assertEqual(out.popleft(), "hihi\n")
    #     self.assertEqual(out.popleft(), "hihi my name\n")
    #     self.assertEqual(len(out), 0)

#     def test_tail(self):
#         out = eval("tail tailTest.txt")
#         self.assertEqual(out.popleft(), "a\n")
#         self.assertEqual(out.popleft(), "b\n")
#         self.assertEqual(out.popleft(), "c\n")
#         self.assertEqual(out.popleft(), "d\n")
#         self.assertEqual(out.popleft(), "e\n")
#         self.assertEqual(out.popleft(), "f\n")
#         self.assertEqual(out.popleft(), "g\n")
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "i\n")
#         self.assertEqual(out.popleft(), "j\n")
#         self.assertEqual(len(out), 0)

#     # def test_tail1(self):
#     #     out = deque()
#     #     eval("tail ./tailTest/tailTest.txt", out)
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(out.popleft(), "b\n")
#     #     self.assertEqual(out.popleft(), "c\n")
#     #     self.assertEqual(out.popleft(), "d\n")
#     #     self.assertEqual(out.popleft(), "e\n")
#     #     self.assertEqual(out.popleft(), "f\n")
#     #     self.assertEqual(out.popleft(), "g\n")
#     #     self.assertEqual(out.popleft(), "h\n")
#     #     self.assertEqual(out.popleft(), "i\n")
#     #     self.assertEqual(out.popleft(), "j\n")
#     #     self.assertEqual(len(out), 0)

#     def test_tail2(self):
#         out = deque()
#         eval("tail -n 2 tailTest.txt", out)
#         self.assertEqual(out.popleft(), "i\n")
#         self.assertEqual(out.popleft(), "j\n")
#         self.assertEqual(len(out), 0)

#     def test_tail3(self):
#         out = deque()
#         eval("tail -n 4 tailTest.txt", out)
#         self.assertEqual(out.popleft(), "g\n")
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "i\n")
#         self.assertEqual(out.popleft(), "j\n")
#         self.assertEqual(len(out), 0)

#     def test_tail4(self):
#         out = deque()
#         eval("tail -n 50 tailTest.txt", out)
#         self.assertEqual(out.popleft(), "hihi\n")
#         self.assertEqual(out.popleft(), "HIHI\n")
#         self.assertEqual(out.popleft(), "hihi my name\n")
#         self.assertEqual(out.popleft(), "a\n")
#         self.assertEqual(out.popleft(), "b\n")
#         self.assertEqual(out.popleft(), "c\n")
#         self.assertEqual(out.popleft(), "d\n")
#         self.assertEqual(out.popleft(), "e\n")
#         self.assertEqual(out.popleft(), "f\n")
#         self.assertEqual(out.popleft(), "g\n")
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "i\n")
#         self.assertEqual(out.popleft(), "j\n")
#         self.assertEqual(len(out), 0)
    
#     def test_tail4(self):
#         out = deque()
#         eval("tail -n 0 tailTest.txt", out)
#         self.assertEqual(len(out), 0)

#     # def test_tail6(self):
#     #     out = deque()
#     #     eval("head < ./tailTest/tail1.txt", out)
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(out.popleft(), "b\n")
#     #     self.assertEqual(out.popleft(), "c\n")
#     #     self.assertEqual(out.popleft(), "d\n")
#     #     self.assertEqual(out.popleft(), "e\n")
#     #     self.assertEqual(out.popleft(), "f\n")
#     #     self.assertEqual(out.popleft(), "g\n")
#     #     self.assertEqual(out.popleft(), "h\n")
#     #     self.assertEqual(out.popleft(), "i\n")
#     #     self.assertEqual(out.popleft(), "j\n")
#     #     self.assertEqual(len(out), 0)

#     # def test_uniq(self):
#     #     out = deque()
#     #     eval("uniq uniq.txt", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(len(out), 0)
    
#     # def test_uniq1(self):
#     #     out = deque()
#     #     eval("uniq ./uniqTest/uniq2.txt", out)
#     #     self.assertEqual(out.popleft(), "apple\n")
#     #     self.assertEqual(out.popleft(), "banana\n")
#     #     self.assertEqual(out.popleft(), "BANANA\n")
#     #     self.assertEqual(out.popleft(), "orange\n")
#     #     self.assertEqual(out.popleft(), "ORANGE\n")
#     #     self.assertEqual(len(out), 0)

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

#     def test_cut(self):
#         out = deque()
#         eval("cut -b 1 ./cutTest/cut1.txt", out)
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "H\n")
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "a\n")
#         self.assertEqual(out.popleft(), "b\n")
#         self.assertEqual(out.popleft(), "c\n")
#         self.assertEqual(out.popleft(), "d\n")
#         self.assertEqual(out.popleft(), "e\n")
#         self.assertEqual(out.popleft(), "f\n")
#         self.assertEqual(out.popleft(), "g\n")
#         self.assertEqual(out.popleft(), "h\n")
#         self.assertEqual(out.popleft(), "i\n")
#         self.assertEqual(out.popleft(), "j\n")
#         self.assertEqual(len(out), 0)

#     def test_cut2(self):
#         out = deque()
#         eval("cut -b 2-3 ./cutTest/cut1.txt", out)
#         self.assertEqual(out.popleft(), "ih\n")
#         self.assertEqual(out.popleft(), "IH\n")
#         self.assertEqual(out.popleft(), "ih\n")
#         self.assertEqual(out.popleft(), "aa\n")
#         self.assertEqual(out.popleft(), "bb\n")
#         self.assertEqual(out.popleft(), "cc\n")
#         self.assertEqual(out.popleft(), "dd\n")
#         self.assertEqual(out.popleft(), "ee\n")
#         self.assertEqual(out.popleft(), "ff\n")
#         self.assertEqual(out.popleft(), "gg\n")
#         self.assertEqual(out.popleft(), "hh\n")
#         self.assertEqual(out.popleft(), "ii\n")
#         self.assertEqual(out.popleft(), "jj\n")
#         self.assertEqual(len(out), 0)

#     def test_cut3(self):
#         out = deque()
#         eval("cut -b 2- ./cutTest/cut1.txt", out)
#         self.assertEqual(out.popleft(), "ihi\n")
#         self.assertEqual(out.popleft(), "IHI\n")
#         self.assertEqual(out.popleft(), "ihi my name\n")
#         self.assertEqual(out.popleft(), "aaaa\n")
#         self.assertEqual(out.popleft(), "bbbb\n")
#         self.assertEqual(out.popleft(), "cccc\n")
#         self.assertEqual(out.popleft(), "dddd\n")
#         self.assertEqual(out.popleft(), "eeee\n")
#         self.assertEqual(out.popleft(), "ffff\n")
#         self.assertEqual(out.popleft(), "gggg\n")
#         self.assertEqual(out.popleft(), "hhhh\n")
#         self.assertEqual(out.popleft(), "iiii\n")
#         self.assertEqual(out.popleft(), "jjjj\n")
#         self.assertEqual(len(out), 0)

#     # def test_cut4(self):
#     #     out = deque()
#     #     eval("cut -b 2-, 3- ./cutTest/cut1.txt", out)
#     #     self.assertEqual(out.popleft(), "ihi\n")
#     #     self.assertEqual(out.popleft(), "IHI\n")
#     #     self.assertEqual(out.popleft(), "ihi my name\n")
#     #     self.assertEqual(out.popleft(), "aaaa\n")
#     #     self.assertEqual(out.popleft(), "bbbb\n")
#     #     self.assertEqual(out.popleft(), "cccc\n")
#     #     self.assertEqual(out.popleft(), "dddd\n")
#     #     self.assertEqual(out.popleft(), "eeee\n")
#     #     self.assertEqual(out.popleft(), "ffff\n")
#     #     self.assertEqual(out.popleft(), "gggg\n")
#     #     self.assertEqual(out.popleft(), "hhhh\n")
#     #     self.assertEqual(out.popleft(), "iiii\n")
#     #     self.assertEqual(out.popleft(), "jjjj\n")
#     #     self.assertEqual(len(out), 0)

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
    

#     #
#     # # REDIRECTION TESTS
#     # def test_input_redirection1(self):
#     #     out = deque()
#     #     eval("cat < ./catTest/cat1.txt", out)
#     #     self.assertEqual(out.popleft(), "this is cat1.\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_input_redirection_infront1(self):
#     #     out = deque()
#     #     eval("< ./catTest/cat1.txt cat", out)
#     #     self.assertEqual(out.popleft(), "this is cat1.\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_input_redirection_nospace1(self):
#     #     out = deque()
#     #     eval("cat <./catTest/cat1.txt", out)
#     #     self.assertEqual(out.popleft(), "this is cat1.\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_output_redirection1(self):
#     #     out = deque()
#     #     eval("echo foo > newfile.txt", out)
#     #     eval("cat newfile.txt", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_output_redirection_overwrite1(self):
#     #     out = deque()
#     #     eval("echo foo > test.txt", out)
#     #     eval("cat test.txt", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # # GLOBBING TESTS
#     # def test_globbing1(self):
#     #     out = deque()
#     #     eval("echo *.txt", out)
#     #     self.assertEqual(out.popleft(), "cutTest.txt findTest.txt grepTest.txt headTest.txt sortTest.txt sorted.txt tailTest.txt test.txt uniqTest.txt\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_globbing_dir1(self):
#     #     out = deque()
#     #     eval("echo catTest *.txt", out)
#     #     self.assertEqual(out.popleft(), "cat1.txt cat2.txt\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # # SEMICOLON TESTS
#     # def test_semoicolon1(self):
#     #     out = deque()
#     #     eval("echo foo; echo bar", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(out.popleft(), "bar\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_semoicolon_chain1(self):
#     #     out = deque()
#     #     eval("echo foo; echo bar; echo foo", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(out.popleft(), "bar\n")
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_semicolon_exception1(self): #to ask
#     #     out = deque()
#     #     eval("ls dir3; echo BBB", out)
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_unsafe_ls1(self):
#     #     out = deque()
#     #     eval("_ls dir3; echo AAA > newfile.txt", out)
#     #     eval("cat newfile.txt", out)
#     #     self.assertEqual(out.popleft(), "AAA\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_pipe_uniq1(self):
#     #     out = deque()
#     #     eval("echo aaa > file2.txt; cat file1.txt file2.txt | uniq -i", out)
#     #     self.assertEqual(out.popleft(), "AAA\n")
#     #     self.assertEqual(out.popleft(), "BBB\n")
#     #     self.assertEqual(out.popleft(), "AAA\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_pipe_chain_sort_uniq1(self):
#     #     out = deque()
#     #     eval("cat file1.txt file2.txt | sort | uniq", out)
#     #     self.assertEqual(out.popleft(), "AAA\n")
#     #     self.assertEqual(out.popleft(), "BBB\n")
#     #     self.assertEqual(out.popleft(), "AAA\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # # SUBSTITUTION TESTS
#     # def test_substitution1(self):
#     #     out = deque()
#     #     eval("echo `echo foo`", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_splitting1(self):
#     #     out = deque()
#     #     eval("echo `echo foo  bar`", out)
#     #     self.assertEqual(out.popleft(), "foo bar\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_insidearg1(self):
#     #     out = deque()
#     #     eval("echo a`echo a`a", out)
#     #     self.assertEqual(out.popleft(), "aaa\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_sortfind1(self):
#     #     out = deque()
#     #     eval("cat `find ./findTest -name '*.txt'` | sort", out)
#     #     self.assertEqual(out.popleft(), "HIHI\n")
#     #     self.assertEqual(out.popleft(), "HIHI\n")
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(out.popleft(), "a\n")
#     #     self.assertEqual(out.popleft(), "b\n")
#     #     self.assertEqual(out.popleft(), "b\n")
#     #     self.assertEqual(out.popleft(), "c\n")
#     #     self.assertEqual(out.popleft(), "c\n")
#     #     self.assertEqual(out.popleft(), "hihi\n")
#     #     self.assertEqual(out.popleft(), "hihi\n")
#     #     self.assertEqual(out.popleft(), "hihi my name\n")
#     #     self.assertEqual(out.popleft(), "hihi my name\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_semicolon1(self):
#     #     out = deque()
#     #     eval("echo `echo foo; echo bar`", out)
#     #     self.assertEqual(out.popleft(), "foo bar\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_keywords1(self):
#     #     out = deque()
#     #     eval("echo `cat test.txt`", out)
#     #     self.assertEqual(out.popleft(), "''")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_app1(self):
#     #     out = deque()
#     #     eval("`echo echo` foo", out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # # QUOTES TESTS
#     # def test_singlequotes1(self):
#     #     out = deque()
#     #     eval("echo 'a b'", out)
#     #     self.assertEqual(out.popleft(), "a b\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_quotekeyword1(self):
#     #     out = deque()
#     #     eval("echo ';'", out)
#     #     self.assertEqual(out.popleft(), ";\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_doublequotes1(self):
#     #     out = deque()
#     #     eval('echo "a b"', out)
#     #     self.assertEqual(out.popleft(), "a b\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_substitution_doublequotes1(self):
#     #     out = deque()
#     #     eval('echo "`echo foo`"', out)
#     #     self.assertEqual(out.popleft(), "foo\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_nested_doublequotes1(self):
#     #     out = deque()
#     #     eval('echo "a `echo "b"`"', out)
#     #     self.assertEqual(out.popleft(), "a b\n")
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_disabled_doublequotes1(self):
#     #     out = deque()
#     #     eval("echo '\"\"'", out)
#     #     self.assertEqual(out.popleft(), '""')
#     #     self.assertEqual(len(out), 0)
#     #
#     # def test_splitting1(self):
#     #     out = deque()
#     #     eval('echo a"b"c', out)
#     #     self.assertEqual(out.popleft(), "abc\n")
#     #     self.assertEqual(len(out), 0)


# if __name__ == "__main__":
#     import sys
#     unittest.main()
