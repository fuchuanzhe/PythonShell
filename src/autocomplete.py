from os import listdir
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


class Autocomplete:
    """
    Autocomplete class provides a command-line interface with auto-completion
    and history features.

    Parameters:
    - apps (dict): A dictionary containing command names as keys.
    - current_dir (str): The current directory for file auto-completion.

    Attributes:
    - commands (list): A list of command names.
    - history (InMemoryHistory): An in-memory history for storing command history.
    - session (PromptSession): A PromptSession instance for interactive command-line input.
    - word_completer (WordCompleter): A WordCompleter instance for auto-completion.

    Methods:
    - __init__: Initializes the Autocomplete instance with the provided applications
      and current directory.
    - update_autocomplete: Updates the auto-completion list if the directory changes.
    - get_history: Returns the in-memory history object.
    - get_session: Returns the prompt session object.
    - get_word_completer: Returns the word completer object.
    """
    def __init__(self, apps, current_dir):
        """
        Initialise Autocomplete instance.

        Parameters:
        - apps (dict): A dictionary containing command names as keys.
        - current_dir (str): The current directory for file auto-completion.
        """
        self.commands = list(apps.keys())
        for x in apps.keys():
            self.commands.append("_" + x)
        self.commands.append("exit")
        self.history = InMemoryHistory()
        self.session = PromptSession(history=self.history, enable_history_search=True)
        self.word_completer = self.update_autocomplete(current_dir)

    def update_autocomplete(self, current_dir):
        """
        Update the auto-completion list whenever the directory changes.

        Parameters:
        - current_dir (str): The new current directory for file auto-completion.

        Returns:
        - WordCompleter: Updated WordCompleter instance.
        """
        keywords = self.commands
        for f in listdir(current_dir):
            if not f.startswith("."):
                keywords.append(f)
        self.word_completer = WordCompleter(keywords)
        return self.word_completer

    def get_history(self):
        """Get the in-memory history object."""
        return self.history

    def get_session(self):
        """Get the prompt session object."""
        return self.session

    def get_word_completer(self):
        """Get the word completer object."""
        return self.word_completer
