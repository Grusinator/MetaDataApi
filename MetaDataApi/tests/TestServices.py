import unittest

# from MetaDataApi.datapoints.services.sound_processing_services import SoundClassifier


class Test_TestServices(unittest.TestCase):
    @unittest.skip("not fully implemented yet")
    def test_sound_classification(self):

        sound_clasifier = SoundClassifier()
        predictions = sound_clasifier.classify_sound(
            r"C:\Users\William\source\repos\web\MetaDataApi\tests\testdata" +
            r"\sample.wav")


if __name__ == '__main__':
    unittest.main()
