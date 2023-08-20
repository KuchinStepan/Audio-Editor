import subprocess
import os
import shutil
import ffmpeg
from progress_saver import ProgressSaver
from audio_editor_dialogs import *
from audio_data import *

inp = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test.mp3'
output = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test_1.mp3'
APPDATA = 'appdata'
ACTIONS_NAME = {Actions.speed: 's', Actions.volume: 'v', Actions.trim: 't',
                Actions.concat: 'c', Actions.reverse: 'r', Actions.partial: 'p'}


def get_length(audio):
    ffmpeg.probe(audio)
    result = ffmpeg.probe(audio)['format']['duration']
    return float(result)


def _create_appdata():
    path = pathlib.Path(APPDATA)
    if not path.exists():
        os.mkdir(APPDATA)


def set_supportive_editor(editor, file_name):
    editor.current_file = file_name
    editor.audio = file_name
    editor.edition_history = EditionHistory('(частичное редактирование)')
    editor.partial_editing = True
    editor.edition_commands = {
        'e': editor.stop,
        '1': editor.change_volume,
        '2': editor.change_speed,
        '3': editor.trim,
        '4': editor.concat,
        'r': editor.reverse,
        'hs': editor.show_history
    }


def trim_function(start, end, inp, out):
    proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-ss', start, '-i', inp, '-to',
                             end, out])
    proc.wait()


def concat_function(first_audio, second_audio, out):
    proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', first_audio, '-i', second_audio,
                             '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1', out])
    proc.wait()


class AudioEditor:
    def __init__(self):
        _create_appdata()
        self.running = False
        self.editing = False
        self.partial_editing = False
        self.current_file = None
        self.audio = None
        self.format = 'mp3'
        self.bin = []
        self.output_name = output
        self.saved = True
        self.edition_history = EditionHistory('отсутствует')

        self.menu_commands = {
            's': self.first_edition,
            'l': self.repeated_edition,
            '0': self.stop
        }

        self.edition_commands = {
            'm': self.back_to_menu,
            '0': self.stop,
            '1': self.change_volume,
            '2': self.change_speed,
            '3': self.trim,
            '4': self.concat,
            '5': self.partial_edition,
            'r': self.reverse,
            'hs': self.show_history,
            's': self.save
        }

    def run(self):
        print('Добро пожаловать в аудио редактор!')
        self.running = True
        self.menu()

    def _get_current_output_filename(self, action: Actions, part=0):
        short_name = self.current_file.split('\\')[-1].split('.')[-2]
        audio_format = self.current_file.split('.')[-1]
        suffix = ACTIONS_NAME[action]
        if action == Actions.partial:
            suffix += str(part)
        if len(self.edition_history.history) == 0:
            path = f'{APPDATA}\\{short_name}_{suffix}.{audio_format}'
        else:
            path = f'{APPDATA}\\{short_name}{suffix}.{audio_format}'
        return path

    def set_output_filename(self):
        path = self.audio.split('.')[-2]
        audio_format = self.audio.split('.')[-1]
        self.output_name = path + '_result.' + audio_format
        i = 1
        while os.path.exists(self.output_name):
            self.output_name = path + f'_result({i}).' + audio_format
            i += 1

    def update_current_file(self, new_name):
        self.saved = False
        self.current_file = new_name
        self.bin.append(new_name)

    def passive_saving(self):
        print('Текущие изменения сохранены, вернутся к редактированию можно в меню')
        saver = ProgressSaver()
        old_audios = saver.delete_old()
        self.clear_bin(exceptional_files=[self.edition_history.history[-1].file_name])
        for name in old_audios:
            os.remove(name)
        saver.add_unfinished(self.audio, self.edition_history)

    def menu(self):
        while self.running:
            print('Введите команду, чтобы продолжить\n')
            show_commands()
            command = read_command(self.menu_commands)
            function = self.menu_commands[command]
            function()

    def back_to_menu(self):
        if not self.saved and not self.partial_editing:
            self.passive_saving()
        self.editing = False

    def stop(self):
        if not self.saved and not self.partial_editing:
            self.passive_saving()
        self.editing = False
        self.running = False
        if not self.partial_editing:
            print('Приложение успешно завершило работу')

    def change_volume(self):
        out = self._get_current_output_filename(Actions.volume)
        volume = read_volume()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.current_file, '-af',
                                 f'volume={volume}', out])
        proc.wait()
        self.update_current_file(out)
        log = Log(Actions.volume, out, volume=volume)
        self.edition_history.add(log)
        print('Громкость успешно изменена\n')

    def change_speed(self):
        out = self._get_current_output_filename(Actions.speed)
        speed = read_speed()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.current_file, '-af',
                                 f'atempo={speed}', out])
        proc.wait()
        self.update_current_file(out)
        log = Log(Actions.speed, out, speed=speed)
        self.edition_history.add(log)
        print('Скорость успешно изменена\n')

    def trim(self):
        out = self._get_current_output_filename(Actions.trim)
        length = get_length(self.current_file)
        time = datetime.timedelta(seconds=int(length), milliseconds=round(length % 1 * 1000))
        start = read_time(f'Введите время начала (общее время аудио: {time})', length)
        end = read_time(f'Введите время конца (общее время аудио: {time})', length)
        trim_function(start, end, self.current_file, out)
        self.update_current_file(out)
        log = Log(Actions.trim, out, start=start, end=end)
        self.edition_history.add(log)
        print('Аудиозапись успешно обрезана\n')

    def concat(self):
        out = self._get_current_output_filename(Actions.concat)
        second_audio = read_audio(True)
        if second_audio == 'm':
            self.back_to_menu()
        else:
            print('Аудиотрек успешно загружен')
        first_audio = self.current_file
        in_order = is_in_order()
        if not in_order:
            first_audio = second_audio
            second_audio = self.current_file

        concat_function(first_audio, second_audio, out)
        self.update_current_file(out)
        log = Log(Actions.concat, out, names=[first_audio, second_audio])
        self.edition_history.add(log)
        print(f'Аудиозаписи {first_audio}, {second_audio} успешно склеены!')

    def partial_edition(self):
        result_out = self._get_current_output_filename(Actions.partial)
        length = get_length(self.current_file)
        time = datetime.timedelta(seconds=int(length), milliseconds=round(length % 1 * 1000))
        start = read_time(f'Введите время начала фрагмента (общее время аудио: {time})', length)
        end = read_time(f'Введите время конца фрагмента (общее время аудио: {time})', length)
        first_part = self._get_current_output_filename(Actions.partial, 1)
        second_part = self._get_current_output_filename(Actions.partial, 2)
        third_part = self._get_current_output_filename(Actions.partial, 3)
        trim_function('00:00:00', start, self.current_file, first_part)
        trim_function(start, end, self.current_file, second_part)
        trim_function(end, str(time), self.current_file, third_part)
        editor = AudioEditor()
        set_supportive_editor(editor, second_part)
        editor.edition(show_partial_edition_commands)

        concat_out_1 = APPDATA + '\\part1.' + self.format

        concat_function(first_part, editor.current_file, concat_out_1)
        concat_function(concat_out_1, third_part, result_out)

        audios_bin = [first_part, second_part, third_part, concat_out_1]
        audios_bin += list(map(lambda x: x.file_name, editor.edition_history.history))
        self.clear_bin(audios_bin)

        self.update_current_file(result_out)
        log = Log(Actions.partial, result_out, start=start, end=end, logs=editor.edition_history.history)
        self.edition_history.add(log)
        print(f'Фрагмент аудиозаписи успешно изменен!')

    def reverse(self):
        out = self._get_current_output_filename(Actions.reverse)
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.current_file, '-af',
                                 'areverse', out])
        proc.wait()
        self.update_current_file(out)
        log = Log(Actions.reverse, out)
        self.edition_history.add(log)
        print('Аудиозапись «развернута»\n')

    def show_history(self):
        self.edition_history.show()
        print()

    def save(self):
        if len(self.edition_history.history) > 0:
            self.set_output_filename()
            shutil.move(self.current_file, self.output_name)
            print('Аудиозапись успешно сохранена')
            print(f'Новое название: {self.output_name}')
            log = Log(Actions.save, self.output_name)
            self.edition_history.add(log)
            self.bin.pop()
            self.saved = True
        else:
            print('Аудиозапись не изменена')

    def load_audio(self):
        self.current_file = 'test.mp3'
        self.audio = self.current_file
        self.edition_history = EditionHistory(self.current_file)
        return

        audio = read_audio()
        self.format = audio.split('.')[-1]
        if audio == 'm':
            self.back_to_menu()
        else:
            self.audio = audio
            self.current_file = audio
            self.edition_history = EditionHistory(self.audio)
            print('Аудиотрек успешно загружен\n')

    def clear_bin(self, files=None, exceptional_files=[]):
        if files is None:
            files = self.bin
        for file in files:
            if file in exceptional_files:
                continue
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        self.bin = []

    def update_from_repeated(self, file):
        saver = ProgressSaver()
        edition_history = saver.pop(file)
        self.audio = file
        self.saved = False
        self.current_file = edition_history.history[-1].file_name
        self.edition_history = edition_history
        for log in edition_history.history:
            self.bin.append(log.file_name)

    def repeated_edition(self):
        saver = ProgressSaver()
        unfinished_files = saver.get_all()
        file = select_file(unfinished_files)
        if file is not None:
            self.update_from_repeated(file)
            self.edition()

    def first_edition(self):
        self.load_audio()
        self.edition()

    def edition(self, edition_commands=show_edition_commands):
        self.editing = True
        while self.editing:
            edition_commands()
            command = read_command(self.edition_commands)
            function = self.edition_commands[command]
            function()
        if self.saved and not self.partial_editing:
            self.clear_bin()
        self.audio = None
