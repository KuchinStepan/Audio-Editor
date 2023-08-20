# Audio-Editor
Audio-Еditor - консольная утилита, позволяющая редактировать аудиозаписи форматов .mp3 и .wav

Чтобы начать редактирование, запустите файл main.py и следуйте инструкциям
В случае выхода в главное меню или завершения работы командой '0' текущие изменения автоматически сохранятся, и Вы сможете продолжить редактирование из главного меню в любой момент.
Для работы утилиты необходимо наличие приложения ffmpeg на вашем устройстве (скачать можно на сайте https://ffmpeg.org), а так же наличие модулей, указаных в 'requirements.txt'


## Структура проекта
- audio_editor.py - Основная логика работы аудиоредактора
- audio_editor_dialogs.py - Набор методов для вывода информации пользователю и сбора от него данных
- audio_data.py - Сохранение и логирование текущих действий пользователя
- progress_saver.py - Сохранение незавершенных редактирований, для изменений через какое-то время
- В папке appdata будут храниться временные файлы, необходимые для работы утилиты

- В папке tests представлены тесты к проекту