import os
import shelve
import os


FILE = 'unsaved.txt'


class ProgressSaver:
    def __init__(self):
        self.file_dict = shelve.open('progress')
        if os.path.exists(FILE):
            with open(FILE, 'r') as f:
                self.unsaved = list(f.read().split())
        else:
            self.unsaved = []
            with open(FILE, 'w'):
                pass

    def get(self, name):
        if name in self.file_dict:
            return self.file_dict[name]
        else:
            return None

    def add_unfinished(self, file_name, edition_history):
        self.unsaved.append(file_name)
        with open(FILE, 'a') as f:
            f.write(file_name + '\n')
        self.file_dict[file_name] = edition_history

    def delete_file(self, file_name):
        self.unsaved.remove(file_name)
        with open(FILE, 'w') as f:
            for name in self.unsaved:
                f.write(name + '\n')
        self.file_dict.pop(file_name)

    def __del__(self):
        self.file_dict.close()
