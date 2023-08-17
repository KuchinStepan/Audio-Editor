import subprocess
import ffmpeg
from audio_editor_dialogs import *
from audio_data import *


inp = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test.mp3'
output = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test_1.mp3'


def get_length(audio):
    ffmpeg.probe(audio)
    result = ffmpeg.probe(audio)['format']['duration']
    return float(result)


class AudioEditor:
    def __init__(self):
        self.running = False
        self.editing = False
        self.audio = None
        self.output_name = output
        self.edition_history = EditionHistory('отсутствует')

        self.menu_commands = {
            's': self.edition,
            'l': 2,
            '0': self.stop
        }

        self.edition_commands = {
            'm': self.back_to_menu,
            '0': self.stop,
            '1': self.change_volume,
            '2': self.change_speed,
            '3': self.trim,

            'r': self.reverse,
            'hs': self.show_history
        }

    def run(self):
        print('Добро пожаловать в аудио редактор!')
        self.running = True
        self.menu()

    def menu(self):
        while self.running:
            print('Введите команду, чтобы продолжить\n')
            show_commands()
            command = read_command(self.menu_commands)
            function = self.menu_commands[command]
            function()

    def back_to_menu(self):
        self.editing = False

    def stop(self):
        self.editing = False
        self.running = False
        print('Приложение успешно завершило работу')

    def change_volume(self):
        volume = read_volume()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 f'volume={volume}', self.output_name])
        proc.wait()
        log = Log(Actions.volume, volume=volume)
        self.edition_history.add(log)
        print('Громкость успешно изменена\n')

    def change_speed(self):
        speed = read_speed()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 f'atempo={speed}', self.output_name])
        proc.wait()
        log = Log(Actions.speed, speed=speed)
        self.edition_history.add(log)
        print('Скорость успешно изменена\n')

    def trim(self):
        length = get_length(self.audio)
        time = datetime.timedelta(seconds=int(length), milliseconds=round(length % 1 * 1000))
        start = read_time(f'Введите время начала (общее время аудио: {time})', length)
        end = read_time(f'Введите время конца (общее время аудио: {time})', length)
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-ss', start, '-i', self.audio, '-to',
                                 end, self.output_name])
        proc.wait()
        log = Log(Actions.trim, start=start, end=end)
        self.edition_history.add(log)
        print('Аудиозапись успешно обрезана\n')

    def merge(self):
        pass

    def reverse(self):
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 'areverse', self.output_name])
        proc.wait()
        log = Log(Actions.reverse)
        self.edition_history.add(log)
        print('Аудиозапись «развернута»\n')

    def show_history(self):
        self.edition_history.show()
        print()

    def load_audio(self):
        self.audio = 'test.mp3'
        self.edition_history = EditionHistory(self.audio)
        return

        audio = read_audio()
        if audio == 'm':
            self.back_to_menu()
        else:
            self.audio = audio
            self.edition_history = EditionHistory(self.audio)
            print('Аудиотрек успешно загружен\n')


    def edition(self):
        self.editing = True
        self.load_audio()
        while self.editing:
            show_edition_commands()
            command = read_command(self.edition_commands)
            function = self.edition_commands[command]
            function()
        self.audio = None
