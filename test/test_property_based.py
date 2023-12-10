from shell import eval

import os
import shutil
from hypothesis import given, strategies as st
import subprocess
import string
import random
import unittest
import shlex


def directory_path_strategy():
    return st.from_regex(r'^[^"\'+`\s]+$', fullmatch=True)



def random_string():
    return st.from_regex(r'^[a-zA-Z0-9]+$', fullmatch=True).map(lambda x: f"{x}")


def pwd_string_strategy():
    return st.builds(lambda random_str: f"pwd {random_str}", random_string())


def echo_string_strategy():
    return st.builds(lambda random_str: f"echo {random_str}", random_string())


def cat_commands_strategy():
    return st.lists(
        elements=st.from_regex(r'^[a-zA-Z0-9]+$', fullmatch=True).map(lambda x: f"{x}.txt"),
        min_size=1,
        max_size=5,
    ).map(lambda args: ['cat'] + args)  # Prepend 'cat' to the arguments


random_string_strategy = st.from_regex(r'^[^"\'+`\s]+$', fullmatch=True)


def create_random_file(file_name):
    # Write 5 random lines of text to the file
    with open(file_name, 'w') as file:
        for _ in range(10):
            random_line = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ') for _ in range(10))
            file.write(random_line + '\n')


def cut_commands_strategy():
    def lines_strategy():
        if random.choice([True, False]):
            return st.integers(min_value=2, max_value=100)  # Single number
        else:
            start = st.integers(min_value=2, max_value=10)
            start1 = st.integers(min_value=2, max_value=10)
            return st.builds(lambda s, e: f"{s}-,{e}-", start, start1)  # Range

    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")

    return st.tuples(lines_strategy(), filename_strategy).map(lambda args: f"cut -b {args[0]} {args[1]}")


def find_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\.txt$', fullmatch=True).map(lambda x: f"{x}")
    return st.builds(lambda filename: f"find . -name {filename}", filename_strategy)


def random_search_string():
    # Generate a random string of length 5 using letters and digits
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))


def grep_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}")
    search_string_strategy = st.builds(random_search_string)

    return st.builds(lambda search_string, filename: f"grep {search_string} {filename}", search_string_strategy, filename_strategy)


def head_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")
    randomNumber_strategy = st.integers(min_value=0, max_value=100)

    return st.builds(lambda randomnumber, filename: f"head -n {randomnumber} {filename}", randomNumber_strategy, filename_strategy)


def sort_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")

    return st.builds(lambda filename: f"sort {filename}", filename_strategy)


def tail_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}.txt")
    randomNumber_strategy = st.integers(min_value=0, max_value=100)

    return st.builds(lambda randomnumber, filename: f"tail -n {randomnumber} {filename}", randomNumber_strategy, filename_strategy)


def uniq_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\$', fullmatch=True).map(lambda x: f"{x}")

    return st.builds(lambda filename: f"uniq {filename}", filename_strategy)


def wc_commands_strategy():
    filename_strategy = st.from_regex(r'^[a-zA-Z0-9]+\.txt$', fullmatch=True).map(lambda x: f"{x}")

    return st.builds(lambda filename: f"wc {filename}", filename_strategy)


class TestPropertyShell(unittest.TestCase):

    def setUp(self):
        # Get the original directory
        self.original_path = os.getcwd()

        # Create a temporary directory for the test
        self.temp_dir = "temp_snapshot_directory"

        # Check if the destination directory exists
        if os.path.exists(self.temp_dir):
            # If it exists, remove it (you can choose another approach if needed)
            shutil.rmtree(self.temp_dir)

        # Create a snapshot of the original directory
        shutil.copytree(self.original_path, self.temp_dir)

        # Change the current working directory to the temporary directory
        os.chdir(self.temp_dir)

    def tearDown(self):
        # Change back to the original directory
        os.chdir(self.original_path)

        # Remove all contents within the temporary directory
        for item in os.listdir(self.temp_dir):
            item_path = os.path.join(self.temp_dir, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        # Explicitly remove any files created during the test in the original directory
        for item in os.listdir(self.original_path):
            if item.endswith(".txt"):
                os.remove(os.path.join(self.original_path, item))

        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)

    @given(ls_args=random_string())
    def test_ls(self, ls_args):
        if not os.path.exists(os.path.join(os.getcwd(), ls_args)):
            with self.assertRaises(FileNotFoundError) or self.assertRaises(ValueError):
                eval(f"ls {ls_args}")
        else:
            print(ls_args)
            # Mock the current working directory
            os.chdir(ls_args)

            # Run eval command
            eval_output = eval("ls")

            # Run the actual ls command
            expected_output = []
            for f in os.listdir(ls_args):
                if not f.startswith("."):
                    expected_output.append(f"{f}\n")

            assert list(eval_output) == expected_output

    @given(ls_args=random_string())
    def test_ls_unsafe(self, ls_args):
        if not os.path.exists(os.path.join(os.getcwd(), ls_args)):
            result = subprocess.run(f"_ls {ls_args}", shell=True, stderr=subprocess.PIPE)

            # Check that the return code indicates an error
            self.assertNotEqual(result.returncode, 0)

            # Check that the error message contains either FileNotFoundError or ValueError
            error_message = result.stderr.decode("utf-8")
            self.assertTrue("FileNotFoundError" in error_message or "ValueError" in error_message)
        else:
            print(ls_args)
            # Mock the current working directory
            os.chdir(ls_args)

            # Run eval command
            eval_output = eval("ls")

            # Run the actual ls command
            expected_output = []
            for f in os.listdir(ls_args):
                if not f.startswith("."):
                    expected_output.append(f"{f}\n")

            assert list(eval_output) == expected_output

    @given(cd_args=directory_path_strategy())
    def test_cd(self, cd_args):
        # Mock the current working directory
        initial_cwd = os.getcwd()
        if not os.path.exists(os.path.join(os.getcwd(), cd_args)) or len(cd_args) == 0:
            with self.assertRaises(FileNotFoundError) or self.assertRaises(ValueError):
                eval(f"cd {cd_args}")
        else:
            eval(f"cd {cd_args}")
            # Validate the change in the current working directory
            expected_cwd = cd_args.split()[0]
            new_cwd = os.getcwd()
            assert new_cwd == os.path.abspath(expected_cwd)

        # Restore the initial working directory
        os.chdir(initial_cwd)

    @given(echo_args=echo_string_strategy())
    def test_echo(self, echo_args):
        eval_output = eval(echo_args)
        process = subprocess.Popen(shlex.split(echo_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        cmdline_output, _ = process.communicate()

        assert ''.join(list(eval_output)) == ''.join(list(cmdline_output))


    @given(pwd_args=pwd_string_strategy())
    def test_pwd(self, pwd_args):
        if len(pwd_args) > 3:
            with self.assertRaises(ValueError) or self.assertRaises(FileNotFoundError):
                eval_output = eval(pwd_args)
        else:
            eval_output = eval(pwd_args)
            process = subprocess.Popen(shlex.split(pwd_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            cmdline_output, _ = process.communicate()
            process.wait()
            print(cmdline_output)

            assert list(eval_output) == list(cmdline_output)

    # Property-based test for eval with "cat" commands
    @given(cat_command=cat_commands_strategy())
    def test_cat(self, cat_command):
        for filename in cat_command[1:]:
            create_random_file(filename)

        # Ensure that the 'eval' function with 'cat' command produces the same output
        eval_output = eval(' '.join(cat_command))

        # Run the 'cat_command' in the command line and capture the output
        process = subprocess.Popen(cat_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmdline_output, _ = process.communicate()
        process.wait()

        flattened_eval_output = [char for word in eval_output for char in word]

        # Assert that the actual output matches the expected output
        assert list(flattened_eval_output) == list(cmdline_output)

    @given(cut_command=cut_commands_strategy())
    def test_cut(self, cut_command):
        _, _, _, filename = cut_command.split()

        create_random_file(filename)

        # Ensure that the 'eval' function with 'cut' command produces the same output
        eval_output = eval(cut_command)

        # Run the 'cut' command using subprocess.run to get the expected output
        process = subprocess.run(shlex.split(cut_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert str(eval_output_str) == expected_output_str

    # Property-based test for eval with "find" commands
    @given(find_command=find_commands_strategy())
    def test_find(self, find_command):
        # Ensure that the 'eval' function with 'find' command produces the same output
        eval_output = eval(find_command)

        # Run the 'find_command' in the command line and capture the output
        process = subprocess.run(shlex.split(find_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str

    # Property-based test for eval with "grep" commands
    @given(grep_command=grep_commands_strategy())
    def test_grep(self, grep_command):
        _, _, filename = grep_command.split()
        create_random_file(filename)

        # Ensure that the 'eval' function with 'grep' command produces the same output
        eval_output = eval(grep_command)

        process = subprocess.run(shlex.split(grep_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str


    # Property-based test for eval with "head" commands
    @given(head_command=head_commands_strategy())
    def test_head(self, head_command):
        _, _, _, filename = head_command.split()
        create_random_file(filename)

        eval_output = eval(head_command)

        process = subprocess.run(shlex.split(head_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str

    # # Property-based test for eval with "sort" commands
    @given(sort_command=sort_commands_strategy())
    def test_sort(self, sort_command):
        _, filename = sort_command.split()
        create_random_file(filename)

        eval_output = eval(sort_command)

        process = subprocess.run(shlex.split(sort_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str

    # Property-based test for eval with "tail" commands
    @given(tail_command=tail_commands_strategy())
    def test_tail(self, tail_command):
        _, _, _, filename = tail_command.split()
        create_random_file(filename)

        eval_output = eval(tail_command)

        process = subprocess.run(shlex.split(tail_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str

    # Property-based test for eval with "uniq" commands
    @given(uniq_command=uniq_commands_strategy())
    def test_uniq(self, uniq_command):
        _, filename = uniq_command.split()
        create_random_file(filename)

        eval_output = eval(uniq_command)

        process = subprocess.run(shlex.split(uniq_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "")

        eval_output_without_newline = [s.replace("\n", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str

    # Property-based test for eval with "wc" commands
    @given(wc_command=wc_commands_strategy())
    def test_wc(self, wc_command):
        _, filename = wc_command.split()
        create_random_file(filename)

        eval_output = eval(wc_command)

        process = subprocess.run(shlex.split(wc_command), capture_output=True, text=True)
        expected_output_str = process.stdout
        expected_output_str = expected_output_str.replace("\n", "").replace(" ", "")

        eval_output_without_newline = [s.replace("\n", "").replace(" ", "") for s in eval_output]

        # Join the modified strings into one big string
        eval_output_str = "".join(eval_output_without_newline)+ filename

        # Assert that the actual output matches the expected output
        assert eval_output_str == expected_output_str