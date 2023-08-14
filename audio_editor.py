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
    print('p   - Воспроизвести «задом наперёд»')
    print('pr  - Воспроизвести «задом наперёд»')
    # print('s   - Сохранить аудио')


def read_command(commands):
    while True:
        command = input()
        if command in commands:
            return command
        else:
            print('Неверно введена команда')


class AudioEditor:
    def __init__(self):
        self.menu_commands = {
            's': self.edition,
            'hs': 1,
            'l': 2,
            '0': self.stop
        }

        self.edition_commands = {
            'm': self.back_to_menu,
            '0': self.stop,
            '2': self.change_speed
        }

        self.running = False
        self.editing = False
        self.audio = None

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

    def stop(self):
        self.editing = False
        self.running = False
        print('Приложение успешно завершило работу')

    def change_speed(self):
        proc = subprocess.Popen(['ffmpeg', '-loglevel', '-8', '-i', self.audio, '-af',
                                 'atempo=2.0', outp])
        proc.wait()
        print('Скорость успешно изменена\n')

    def load_audio(self):
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

    def back_to_menu(self):
        self.editing = False

    def edition(self):
        self.editing = True
        self.load_audio()
        while self.editing:
            show_edition_commands()
            command = read_command(self.edition_commands)
            function = self.edition_commands[command]
            function()
        self.audio = None
