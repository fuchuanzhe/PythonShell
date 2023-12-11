from os import listdir
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


class Autocomplete:
    def __init__(self, apps, current_dir):
        self.commands = list(apps.keys())
        for x in apps.keys():
            self.commands.append("_" + x)
        self.commands.append("exit")
        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history, enable_history_search=True)
        self.word_completer = self.update_autocomplete(current_dir)

    def update_autocomplete(self, current_dir):
        keywords = self.commands
        for f in listdir(current_dir):
            if not f.startswith("."):
                keywords.append(f)
        self.word_completer = WordCompleter(keywords)
        return self.word_completer

    def get_history(self):
        return self.history

    def get_session(self):
        return self.session

    def get_completer(self):
        return self.word_completer
