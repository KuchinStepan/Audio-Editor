import enum


class Actions(enum.Enum):
    volume = 1
    speed = 2
    trim = 3
    merge = 4
    reverse = 5
    partial = 6


class Log:
    def __init__(self, action: Actions, **kwargs):
        self.action = action
        self.values = dict()
        for key in kwargs.keys():
            self.values[key] = kwargs[key]
        self._set_string_preview()

    def _set_string_preview(self):
        result = 'Ошибка лога'
        try:
            match self.action:
                case Actions.volume:
                    volume = self.values['volume']
                    result = f'Изменение громкости на {volume}'
                case Actions.speed:
                    speed = self.values['speed']
                    result = f'Изменение скорости на {speed}'
                case Actions.trim:
                    start = self.values['start']
                    end = self.values['end']
                    result = f'Аудиозапись обрезана с {start} по {end}'
                case Actions.reverse:
                    result = f'Реверс аудиозаписи'
                case Actions.merge:
                    names = ', '.join(self.values['names'])
                    result = f'Склеены аудиозаписи: {names}'
                case Actions.partial:
                    start = self.values['start']
                    end = self.values['end']
                    logs = '- ' + '\n- '.join(map(str, self.values['logs']))
                    result = f'В фрагменте с {start} по {end} следующие изменения:\n{logs}\n' \
                             f'__________________'
        except KeyError:
            result = 'Ошибка лога'
        self.preview = result

    def __str__(self):
        return self.preview


class EditionHistory:
    def __init__(self, name):
        self.name = name
        self.history = []

    def show(self):
        audio = self.name.split('\\')[-1].split('/')[-1]
        if len(self.history) == 0:
            audio += ' отсутствует'
        print(f'История изменений в аудио {audio}:')
        for log in self.history:
            print(log)

    def add(self, log: Log):
        self.history.append(log)
