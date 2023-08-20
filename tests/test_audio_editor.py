from audio_editor import *
import unittest


AUDIO = 'test.mp3'


class TestAudioData(unittest.TestCase):
    def setUp(self):
        self.editor = AudioEditor()
        self.editor.audio = AUDIO
        self.editor.current_file = AUDIO

    def testGetLength(self):
        length = get_length(AUDIO)
        self.assertEqual(15.438313, length)

    def testGetCurrentOutputName(self):
        result = self.editor._get_current_output_filename(Actions.volume)
        expected = 'appdata\\test_v.mp3'
        self.assertEqual(expected, result)

    def testSetOutputName(self):
        self.editor.set_output_filename()
        expected = 'test_result.mp3'
        self.assertEqual(expected, self.editor.output_name)

    def testUpdateCurrentFile(self):
        new = 'appdata\\test_v.mp3'
        self.editor.update_current_file(new)
        self.assertEqual('appdata\\test_v.mp3', self.editor.current_file)
        self.assertFalse(self.editor.saved)
        self.assertEqual(1, len(self.editor.bin))

    def testStop(self):
        self.editor.partial_editing = True
        self.editor.editing = True
        self.editor.running = True
        self.editor.stop()
        self.assertFalse(self.editor.editing)
        self.assertFalse(self.editor.running)


if __name__ == '__main__':
    unittest.main()
