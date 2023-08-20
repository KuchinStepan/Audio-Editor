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

    def get_all(self):
        result = set(self.unsaved)
        return result

    def delete_old(self):
        old_audios = []
        count = len(self.file_dict)
        if count >= 3:
            for i in range(0, count - 3):
                name = self.unsaved[i]
                history = self.get(name)
                for log in history.history:
                    old_audios.append(log.file_name)
                self.delete_file(name)
        return old_audios

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

    def pop(self, file_name):
        result = self.get(file_name)
        self.delete_file(file_name)
        return result

    def clear(self):
        with open(FILE, 'w'):
            pass
        self.file_dict.clear()

    def __del__(self):
        self.file_dict.close()
