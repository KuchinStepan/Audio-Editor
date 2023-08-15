import subprocess
import pathlib


inp = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test.mp3'
outp = 'C:\\Users\\Степан\\Desktop\\Python\\Audio-Editor\\test_1.mp3'


def show_commands():
    print('s    - Начать редактирование')
    print('hs   - Просмотреть историю изменений')
    print('l    - Продолжить незавершенное редактирование')
    print('0    - Завершить работу')


def show_edition_commands():
    print('m   - Вернуться в главное меню')
    print('0   - Завершить работу')
    print('1   - Изменить громкость')
    print('2   - Изменить скорость')
    print('3   - Вырезать фрагмент')
    print('4   - Склеить фрагменты')
    print('5   - Изменить конкретную часть текущего аудио')
    print('r   - «Развернуть» аудиозапись (реверс)')
    print('s   - Сохранить аудио')


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
        except ValueError as e:
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
        except ValueError as e:
            print('Неверно введено значение! (Попробуйте заменить «,» на «.»)')
        else:
            if volume > 0:
                success = True
            else:
                print('Число вне диапозона!')
    return volume


class AudioEditor:
    def __init__(self):
        self.running = False
        self.editing = False
        self.audio = None
        self.output_name = outp

        self.menu_commands = {
            's': self.edition,
            'hs': 1,
            'l': 2,
            '0': self.stop
        }

        self.edition_commands = {
            'm': self.back_to_menu,
            '0': self.stop,
            '1': self.change_volume,
            '2': self.change_speed,

            'r': self.reverse
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
        print('Громкость успешно изменена\n')

    def change_speed(self):
        speed = _read_speed()
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 f'atempo={speed}', self.output_name])
        proc.wait()
        print('Скорость успешно изменена\n')

    def reverse(self):
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 'areverse', self.output_name])
        proc.wait()
        print('Аудиозапись «развернута»\n')

    def load_audio(self):
        self.audio = 'test.mp3'
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
