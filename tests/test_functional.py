import os
from audio_editor import *
import unittest
import scipy.io.wavfile as wav
import numpy as np


AUDIO = 'test.mp3'
DATA = 'tests\\appdata'


class TestAudioData(unittest.TestCase):
    def setUp(self):
        self.editor = AudioEditor()
        self.editor.audio = AUDIO
        self.editor.current_file = AUDIO
        self.editor.running = True

    def testTrim(self):
        output = 'out_trim.mp3'
        trim_function('00:00:00', '00:00:03', self.editor.current_file, output)

        result_length = get_length(output)
        os.remove(output)
        self.assertAlmostEqual(3, result_length, 1)

    def testConcat(self):
        output = 'out_concat.mp3'
        start_length = get_length(self.editor.current_file)
        concat_function(self.editor.current_file, self.editor.current_file, output)

        result_length = get_length(output)
        os.remove(output)
        self.assertAlmostEqual(start_length * 2, result_length, 1)

    def testSpeed(self):
        output = 'out_speed.mp3'
        start_length = get_length(self.editor.current_file)
        speed_function(self.editor.current_file, 2.0, output)
        result_length = get_length(output)
        os.remove(output)
        self.assertAlmostEqual(start_length / 2, result_length, places=1)

    def testVolume(self):
        audio = 'test.wav'
        output = 'out_volume.wav'

        sample_rate, audio_data = wav.read(audio)
        max_value = np.max(audio_data)
        start_max_db = 10 * np.log10(max_value / 20e-6)
        self.assertTrue(start_max_db > 0)

        volume_function(audio, 0.0, output)

        sample_rate, audio_data = wav.read(output)
        max_value = np.max(audio_data)
        end_max_db = 10 * np.log10(max_value / 20e-6)
        os.remove(output)
        self.assertEqual('-inf', str(end_max_db))

    def testReverse(self):
        audio = 'test.wav'
        output = 'appdata\\test_r.wav'
        self.editor.current_file = 'test.wav'

        _, excpected_data = wav.read('expected_reverse.wav')
        self.editor.reverse()
        _, end_audio_data = wav.read(audio)

        dif_set = {0}
        for i in range(min(len(excpected_data), len(end_audio_data))):
            if abs(excpected_data[i][0] - end_audio_data[i][0]) < 7:
                continue

        os.remove(output)
        self.assertEqual({0}, dif_set)


if __name__ == '__main__':
    unittest.main()
