from shell import eval

import os
import shutil
from hypothesis import given, strategies as st
import subprocess
import string
import random
import unittest
import shlex
from unittest.mock import patch
from io import StringIO


def random_string():
    return st.from_regex(
        r'^[a-zA-Z0-9]+$', fullmatch=True
    ).map(lambda x: f"{x}")


def cat_commands_strategy():
    return st.lists(
        elements=st.from_regex(
            r'^[a-zA-Z0-9]+$', fullmatch=True).map(lambda x: f"{x}.txt"),
        min_size=1,
        max_size=5,
    ).map(lambda args: ['cat'] + args)


def get_filenames_in_current_directory():
    current_directory = os.getcwd()
    return [filename for filename in os.listdir(current_directory)
            if os.path.isfile(filename)]


@st.composite
def non_matching_strings(draw):
    filenames = get_filenames_in_current_directory()

    while True:
        generated_string = draw(st.from_regex(
            r'^[a-zA-Z0-9]+$', fullmatch=True))
        if all(filename not in generated_string for filename in filenames):
            return generated_string


def create_random_file(file_name):
    # Write 10 random lines of text to the file
    with open(file_name, 'w') as file:
        for _ in range(10):
            random_line = ''.join(random.choice(
                string.ascii_letters +
                string.digits + string.punctuation + ' ') for _ in range(10))
            file.write(random_line + '\n')


def cut_commands_strategy():
    def lines_strategy():
        return st.integers(min_value=2, max_value=100)
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")
    return st.tuples(lines_strategy(), filename_strategy) \
        .map(lambda args: f"cut -b {args[0]} {args[1]}")


def find_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\.txt$', fullmatch=True).map(lambda x: f"{x}")
    return st.builds(lambda filename: f"find . -name {filename}",
                     filename_strategy)


def random_search_string():
    # Generate a random string of length 5 using letters and digits
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(5))


def grep_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}")
    search_string_strategy = st.builds(random_search_string)

    return st.builds(lambda search_string, filename:
                     f"grep {search_string} {filename}",
                     search_string_strategy, filename_strategy)


def head_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")
    randomNumber_strategy = st.integers(min_value=0, max_value=100)

    return st.builds(lambda randomnumber, filename:
                     f"head -n {randomnumber} {filename}",
                     randomNumber_strategy, filename_strategy)


def sort_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")

    return st.builds(lambda filename: f"sort {filename}", filename_strategy)


def tail_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")
    randomNumber_strategy = st.integers(min_value=0, max_value=100)

    return st.builds(lambda randomnumber, filename:
                     f"tail -n {randomnumber} {filename}",
                     randomNumber_strategy, filename_strategy)


def uniq_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}")

    return st.builds(lambda filename: f"uniq {filename}", filename_strategy)


def wc_commands_strategy():
    filename_strategy = st.from_regex(
        r'^[a-zA-Z0-9]+\.txt$', fullmatch=True).map(lambda x: f"{x}")

    return st.builds(lambda filename: f"wc {filename}", filename_strategy)


class TestPropertyShell(unittest.TestCase):

    def setUp(self):
        self.created_files = []
        self.original_path = os.getcwd()
        self.temp_dir = "temp_snapshot_directory"

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        def ignore_venv(src, names):
            return set(names) & {'venv'}

        # Create a snapshot of the original directory, excluding venv
        shutil.copytree(self.original_path, self.temp_dir, ignore=ignore_venv)
        os.chdir(self.temp_dir)

    def tearDown(self):
        # Change back to the original directory
        os.chdir(self.original_path)

        # Remove only the contents within the temporary directory
        # created during the test
        for item in os.listdir(self.temp_dir):
            item_path = os.path.join(self.temp_dir, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        # Remove the temporary directory
        shutil.rmtree("temp_snapshot_directory")

    @given(ls_args=random_string())
    def test_ls(self, ls_args):
        if not os.path.exists(os.path.join(os.getcwd(), ls_args)):
            with self.assertRaises(FileNotFoundError) or \
                 self.assertRaises(ValueError):
                eval(f"ls {ls_args}")
        else:
            os.chdir(ls_args)
            eval_output = eval("ls")

            expected_output = []
            for f in os.listdir(ls_args):
                if not f.startswith("."):
                    expected_output.append(f"{f}\n")

            assert list(eval_output) == expected_output

    @patch('sys.stdout', new_callable=StringIO)
    @given(ls_args=random_string())
    def test_ls_unsafe(self, ls_args, mock_stdout):
        if not os.path.exists(os.path.join(os.getcwd(), ls_args)):
            eval(f"_ls {ls_args}")
            result = mock_stdout.getvalue()
            self.assertIn("Errno 2", result)
        else:
            os.chdir(ls_args)
            eval_output = eval("ls")

            expected_output = []
            for f in os.listdir(ls_args):
                if not f.startswith("."):
                    expected_output.append(f"{f}\n")

            assert list(eval_output) == expected_output

    @given(cd_args=random_string())
    def test_cd(self, cd_args):
        initial_cwd = os.getcwd()
        if not os.path.exists(os.path.join(os.getcwd(), cd_args)):
            # Check that cd raises an error if the directory does not exist
            # or invalid command line arguments are passed
            with self.assertRaises(FileNotFoundError) or \
                 self.assertRaises(ValueError):
                eval(f"cd {cd_args}")
        else:
            eval(f"cd {cd_args}")
            expected_cwd = cd_args.split()[0]
            new_cwd = os.getcwd()
            assert new_cwd == os.path.abspath(expected_cwd)

        os.chdir(initial_cwd)

    @patch('sys.stdout', new_callable=StringIO)
    @given(cd_args=random_string())
    def test_cd_unsafe(self, cd_args, mock_stdout):
        initial_cwd = os.getcwd()
        if not os.path.exists(os.path.join(os.getcwd(), cd_args)):
            eval(f"_cd {cd_args}")
            result = mock_stdout.getvalue()
            self.assertIn("Errno 2", result)
        else:
            eval(f"_cd {cd_args}")
            expected_cwd = cd_args.split()[0]
            new_cwd = os.getcwd()
            assert new_cwd == os.path.abspath(expected_cwd)

        os.chdir(initial_cwd)

    @given(echo_args=random_string())
    def test_echo(self, echo_args):
        eval_output = eval(f"echo {echo_args}")

        # Run the echo command in the command line and capture the output
        process = subprocess.Popen(shlex.split(
            f"echo {echo_args}"), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        cmdline_output, _ = process.communicate()

        assert ''.join(list(eval_output)) == ''.join(list(cmdline_output))

    @given(pwd_args=random_string())
    def test_pwd(self, pwd_args):
        if len(pwd_args) > 0:
            with self.assertRaises(ValueError) or \
                 self.assertRaises(FileNotFoundError):
                eval_output = eval(f"pwd {pwd_args}")
        else:
            eval_output = eval(pwd_args)
            # Run the pwd command in the command line and capture the output
            process = subprocess.Popen(shlex.split(f"pwd {pwd_args}"),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            cmdline_output, _ = process.communicate()
            process.wait()
            print(cmdline_output)

            assert list(eval_output) == list(cmdline_output)

    @patch('sys.stdout', new_callable=StringIO)
    @given(pwd_args=random_string())
    def test_pwd_unsafe(self, pwd_args, mock_stdout):
        if len(pwd_args) > 0:
            eval_output = eval(f"_pwd {pwd_args}")
            result = mock_stdout.getvalue()
            self.assertIn("Invalid command line arguments", result)
        else:
            eval_output = eval(pwd_args)
            # Run the pwd command in the command line and capture the output
            process = subprocess.Popen(shlex.split(f"pwd {pwd_args}"),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            cmdline_output, _ = process.communicate()
            process.wait()
            print(cmdline_output)

            assert list(eval_output) == list(cmdline_output)

    @given(cat_command=cat_commands_strategy())
    def test_cat(self, cat_command):
        for filename in cat_command[1:]:
            create_random_file(filename)
            self.created_files.append(os.path.join(os.getcwd(), filename))

        eval_output = eval(' '.join(cat_command))

        # Run the cat_command in the command line and capture the output
        process = subprocess.Popen(
            cat_command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        cmdline_output, _ = process.communicate()
        process.wait()

        flattened_eval_output = [char for word in eval_output for char in word]
        assert list(flattened_eval_output) == list(cmdline_output)

    @patch('sys.stdout', new_callable=StringIO)
    @given(cat_command=random_string())
    def test_cat_unsafe(self, cat_command, mock_stdout):
        eval(f"_cat {cat_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(cut_command=cut_commands_strategy())
    def test_cut(self, cut_command):
        _, _, _, filename = cut_command.split()

        create_random_file(filename)

        eval_output = eval(cut_command)

        # Run the cut_command using subprocess.run to get the expected output
        process = subprocess.run(shlex.split(
            cut_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert str(eval_output_str) == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(cut_command=non_matching_strings())
    def test_cut_unsafe(self, cut_command, mock_stdout):
        eval(f"_cut -b 2 {cut_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(find_command=find_commands_strategy())
    def test_find(self, find_command):
        eval_output = eval(find_command)

        # Run the find_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            find_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(find_command=non_matching_strings())
    def test_find_unsafe(self, find_command, mock_stdout):
        eval(f"_find {find_command} -name {find_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(grep_command=grep_commands_strategy())
    def test_grep(self, grep_command):
        _, _, filename = grep_command.split()
        create_random_file(filename)

        eval_output = eval(grep_command)

        # Run the grep_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            grep_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(grep_command=non_matching_strings())
    def test_grep_unsafe(self, grep_command, mock_stdout):
        search_string = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(5))
        eval(f"_grep {search_string} {grep_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(head_command=head_commands_strategy())
    def test_head(self, head_command):
        _, _, _, filename = head_command.split()
        create_random_file(filename)

        eval_output = eval(head_command)

        # Run the head_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            head_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(head_command=non_matching_strings())
    def test_head_unsafe(self, head_command, mock_stdout):
        randomNumber = st.integers(min_value=0, max_value=100)

        eval(f"_head -n {randomNumber} {head_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Invalid command line arguments", result)

    @given(sort_command=sort_commands_strategy())
    def test_sort(self, sort_command):
        _, filename = sort_command.split()
        create_random_file(filename)

        eval_output = eval(sort_command)

        # Run the sort_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            sort_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(sort_command=non_matching_strings())
    def test_sort_unsafe(self, sort_command, mock_stdout):
        eval(f"_sort {sort_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(tail_command=tail_commands_strategy())
    def test_tail(self, tail_command):
        _, _, _, filename = tail_command.split()
        create_random_file(filename)

        eval_output = eval(tail_command)

        # Run the tail_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            tail_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(tail_command=non_matching_strings())
    def test_tail_unsafe(self, tail_command, mock_stdout):
        randomNumber = st.integers(min_value=0, max_value=100)
        eval(f"_tail -n {randomNumber} {tail_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Invalid command line arguments", result)

    @given(uniq_command=uniq_commands_strategy())
    def test_uniq(self, uniq_command):
        _, filename = uniq_command.split()
        create_random_file(filename)

        eval_output = eval(uniq_command)

        # Run the uniq_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            uniq_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [
            s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(uniq_command=non_matching_strings())
    def test_uniq_unsafe(self, uniq_command, mock_stdout):
        eval(f"_uniq {uniq_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)

    @given(wc_command=wc_commands_strategy())
    def test_wc(self, wc_command):
        _, filename = wc_command.split()
        create_random_file(filename)

        eval_output = eval(wc_command)

        # Run the wc_command in the command line and capture the output
        process = subprocess.run(shlex.split(
            wc_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace(
            "\n", "").replace(" ", "")

        eval_output_without_newline = [
            s.replace("\n", "").replace(" ", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline) + filename
        assert eval_output_str == expected_output_str

    @patch('sys.stdout', new_callable=StringIO)
    @given(wc_command=non_matching_strings())
    def test_wc_unsafe(self, wc_command, mock_stdout):
        eval(f"_wc {wc_command}")
        result = mock_stdout.getvalue()
        self.assertIn("Errno 2", result)
