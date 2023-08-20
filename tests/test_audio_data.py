from audio_data import Actions, Log, EditionHistory
import unittest


AUDIO = 'test.mp3'


class TestAudioData(unittest.TestCase):
    def testVolumeLog(self):
        log = Log(Actions.volume, AUDIO, volume=2)
        expected = 'Изменение громкости на 2'
        self.assertEqual(expected, str(log))

    def testTrimLog(self):
        log = Log(Actions.trim, AUDIO, start='00:00:00', end='00:00:10')
        expected = 'Аудиозапись обрезана с 00:00:00 по 00:00:10'
        self.assertEqual(expected, str(log))

    def testPartialLog(self):
        volume_log = Log(Actions.volume, AUDIO, volume=2)
        trim_log = Log(Actions.trim, AUDIO, start='00:00:00', end='00:00:10')
        partial_log = Log(Actions.partial, AUDIO, start='00:00:00', end='00:00:14', logs=[volume_log, trim_log])
        expected = 'В фрагменте с 00:00:00 по 00:00:14 следующие изменения:\n' \
                   '- Изменение громкости на 2\n' \
                   '- Аудиозапись обрезана с 00:00:00 по 00:00:10\n' \
                   '__________________'
        self.assertEqual(expected, str(partial_log))

    def testAddEditionHistory(self):
        history = EditionHistory(AUDIO)
        log = Log(Actions.volume, AUDIO, volume=2)
        history.add(log)
        self.assertEqual(1, len(history.history))

    def testPopEditionHistory(self):
        history = EditionHistory(AUDIO)
        log = Log(Actions.volume, AUDIO, volume=2)
        history.add(log)
        log_out = history.pop()
        self.assertEqual(0, len(history.history))
        self.assertEqual(log, log_out)


if __name__ == '__main__':
    unittest.main()
