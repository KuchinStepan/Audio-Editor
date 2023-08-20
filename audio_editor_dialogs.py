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
    print('s   - Сохранить аудио')


def show_partial_edition_commands():
    print('e   - Завершить частичное редактирование')
    print('1   - Изменить громкость')
    print('2   - Изменить скорость')
    print('3   - Обрезать аудиозапись')
    print('4   - Склеить с другой аудиозаписью')
    print('r   - «Развернуть» аудиозапись (реверс)')
    print('hs  - Просмотреть историю изменений')


def read_command(commands):
    while True:
        command = input()
        if command.lower() in commands:
            return command
        else:
            print('Неверно введена команда')


def read_audio(for_merge=False):
    message = ''
    if for_merge:
        message = ' второго'
    while True:
        print(f'Введите название{message} аудиотрека (формат: .mp3, .wav) или напишите "m" чтобы вернуться в меню')
        audio = input()
        if audio == 'm':
            return audio
        p = pathlib.Path(audio)
        if p.exists():
            if audio.split('.')[-1] in ['mp3', 'wav']:
                return audio
            else:
                print('Неверное разрешение аудиотрека! Попробуйте .mp3 или .wav')
        else:
            print(f'Аудиотрек {audio} не найден!')


def select_file(filenames):
    filenames = list(filenames)
    if len(filenames) == 0:
        print('Нет несохраненных файлов')
        return None
    print('Выберите файл, с которым хотите продолжить работу')
    success = False
    while not success:
        for i in range(len(filenames)):
            print(f'{i+1} - {filenames[i]}')
        try:
            ans = int(input())
            if 1 <= ans <= len(filenames):
                return filenames[ans - 1]
            else:
                print('Неверно введено значение')
        except ValueError:
            print('Неверно введено значение')


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
            if volume >= 0:
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
                    ms = float(f'0.{time[1]}')
                    right_format = True
                except ValueError:
                    print('Неверно введено значение!')
            elif len(time) > 2:
                print('Неверно введено значение!')

            if right_format:
                timedelta = datetime.timedelta(hours=parsed_time.hour, minutes=parsed_time.minute,
                                               seconds=parsed_time.second, milliseconds=ms * 1000)
                seconds = timedelta.total_seconds()
                if seconds <= limit:
                    success = True
                else:
                    print('Неверно указан диапазон!')
    return '.'.join(time)


def is_in_order():
    success = False
    while not success:
        print('Склеить аудиозаписи в порядке их добавления(1) или обратном(2)?')
        ans = input()
        if ans.lower() == '1':
            return True
        elif ans.lower() == '2':
            return False
        else:
            print('Неверно введена команда')
