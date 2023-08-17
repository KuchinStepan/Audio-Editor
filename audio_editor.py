import subprocess
import pathlib
import ffmpeg
import datetime
from audio_data import *


inp = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test.mp3'
output = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test_1.mp3'


def show_commands():
    print('s    - Начать редактирование')
    print('l    - Продолжить незавершенное редактирование')
    print('0    - Завершить работу')


def show_edition_commands():
    print('m   - Вернуться в главное меню')
    print('0   - Завершить работу')
    print('1   - Изменить громкость')
    print('2   - Изменить скорость')
    print('3   - Обрезать аудиозапись')
    print('4   - Склеить фрагменты')
    print('5   - Изменить конкретную часть текущего аудио')
    print('r   - «Развернуть» аудиозапись (реверс)')
    print('hs  - Просмотреть историю изменений')
    # print('s   - Сохранить аудио')


def read_command(commands):
    while True:
        command = input()
        if command.lower() in commands:
            return command
        else:
            print('Неверно введена команда')


def _read_speed():
    success = False
    speed = 1.0
    while not success:
        try:
            print('Введите новую скорость воспроизведения в диапозоне от 0.5 до 2.0')
            speed = float(input())
        except ValueError:
            print('Неверно введено значение! (Попробуйте заменить «,» на «.»)')
        else:
            if 0.5 <= speed <= 2.0:
                success = True
            else:
                print('Число вне диапозона!')
    return speed


def _read_volume():
    success = False
    volume = 1.0
    print('Текущая громкость: 1.0')
    while not success:
        try:
            print('Введите новую громкость воспроизведения (значение >= 0)')
            volume = float(input())
        except ValueError:
            print('Неверно введено значение! (Попробуйте заменить «,» на «.»)')
        else:
            if volume > 0:
                success = True
            else:
                print('Число вне диапозона!')
    return volume


def _read_time(message, limit):
    success = False
    time = '00:00:00'
    while not success:
        try:
            print(f'{message}\nФормат - hh:mm:ss или hh:mm:ss.ms')
            time = input().split('.')
            parsed_time = datetime.time.fromisoformat(time[0])
        except ValueError:
            print('Неверно введено значение!')
        else:
            right_format = False
            ms = 0
            if len(time) == 1:
                right_format = True
            elif len(time) == 2:
                try:
                    ms = int(time[1])
                    right_format = True
                except ValueError:
                    print('Неверно введено значение!')
            elif len(time) > 2:
                print('Неверно введено значение!')

            if right_format:
                timedelta = datetime.timedelta(hours=parsed_time.hour, minutes=parsed_time.minute,
                                               seconds=parsed_time.second, milliseconds=ms * 100)
                seconds = timedelta.total_seconds()

                if seconds <= limit:
                    success = True
                else:
                    print('Неверно указан диапазон!')
    return '.'.join(time)


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
        volume = _read_volume()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 f'volume={volume}', self.output_name])
        proc.wait()
        log = Log(Actions.volume, volume=volume)
        self.edition_history.add(log)
        print('Громкость успешно изменена\n')

    def change_speed(self):
        speed = _read_speed()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 f'atempo={speed}', self.output_name])
        proc.wait()
        log = Log(Actions.speed, speed=speed)
        self.edition_history.add(log)
        print('Скорость успешно изменена\n')

    def trim(self):
        length = get_length(self.audio)
        time = datetime.timedelta(seconds=int(length), milliseconds=round(length % 1 * 1000))
        start = _read_time(f'Введите время начала (общее время аудио: {time})', length)
        end = _read_time(f'Введите время конца (общее время аудио: {time})', length)
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-ss', start, '-i', self.audio, '-to',
                                 end, self.output_name])
        proc.wait()
        log = Log(Actions.trim, start=start, end=end)
        self.edition_history.add(log)
        print('Аудиозапись успешно обрезана\n')

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
        loaded = False
        while not loaded:
            print('Введите название аудиотрека (формат: .mp3, .wav) или напишите "m" чтобы вернуться в меню')
            audio = input()
            if audio == 'm':
                self.back_to_menu()
                break
            p = pathlib.Path(audio)
            if p.exists():
                if audio.split('.')[-1] in ['mp3', 'wav']:
                    self.audio = audio
                    self.edition_history = EditionHistory(self.audio)
                    print('Аудиотрек успешно загружен\n')
                    loaded = True
                else:
                    print('Неверное разрешение аудиотрека! Попробуйте .mp3 или .wav')
            else:
                print(f'Аудиотрек {audio} не найден!')

    def edition(self):
        self.editing = True
        self.load_audio()
        while self.editing:
            show_edition_commands()
            command = read_command(self.edition_commands)
            function = self.edition_commands[command]
            function()
        self.audio = None
