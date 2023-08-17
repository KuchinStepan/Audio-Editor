import datetime
import pathlib


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
    print('4   - Склеить с другой аудиозаписью')
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


def read_audio():
    while True:
        print('Введите название аудиотрека (формат: .mp3, .wav) или напишите "m" чтобы вернуться в меню')
        audio = input()
        if audio == 'm':
            return audio
        p = pathlib.Path(audio)
        if p.exists():
            if audio.split('.')[-1] in ['mp3', 'wav']:
                print('Аудиотрек успешно загружен\n')
                return audio
            else:
                print('Неверное разрешение аудиотрека! Попробуйте .mp3 или .wav')
        else:
            print(f'Аудиотрек {audio} не найден!')


def read_speed():
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


def read_volume():
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


def read_time(message, limit):
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
