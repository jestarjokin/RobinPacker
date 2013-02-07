import array
import unittest

import robinpacker.packers.gfx

class TestGfxRleEncoder(unittest.TestCase):
    def setUp(self):
        class MockGfxData(object):
            def __init__(self):
                self.data = None
        self.gfx_data = MockGfxData()

    def _process(self, input, expected):
        self.gfx_data.data = array.array('B', input)
        expected = array.array('B', expected)
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testRepeatingValues(self):
        input = [1, 1, 1]
        expected = [0x83, 1, 0xFF, 0xFF]
        self._process(input, expected)

    def testManyRepeatingValues(self):
        input = [1] * 0x80
        expected = [0xFE, 1, 0x82, 1, 0xFF, 0xFF] # can't use 0xFF
        self._process(input, expected)

    def testMultipleRepeatingValues(self):
        input = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3]
        expected = [0x85, 1, 0x84, 2, 0x83, 3, 0xFF, 0xFF]
        self._process(input, expected)

    def testDiscreteValues(self):
        input = [1, 2, 3]
        expected = [0x03, 1, 2, 3, 0xFF, 0xFF]
        self._process(input, expected)

    def testManyDiscreteValues(self):
        input = [1, 2, 3] * 43
        expected = [0x7F] + [1, 2, 3] * 42 + [1, 0x02, 2, 3, 0xFF, 0xFF] # not sure if 0x7F is okay, or if it should be 0x7E
        self._process(input, expected)

    def testMultipleDiscreteValuesWithRepeatingValuesInTheMiddle(self):
        input = [1, 2, 3, 4, 4, 4, 5, 6, 7]
        expected = [0x03, 1, 2, 3, 0x83, 4, 0x03, 5, 6, 7, 0xFF, 0xFF]
        self._process(input, expected)

    def testMultipleRepeatingValuesWithDiscreteValuesInTheMiddle(self):
        input = [1, 1, 1, 2, 3, 4, 4, 4, 4]
        expected = [0x83, 1, 0x02, 2, 3, 0x84, 4, 0xFF, 0xFF]
        self._process(input, expected)

    def testTrailingZeroValuesAreOmittedRepeating(self):
        input = [1, 1, 1, 2, 3, 0, 0, 0, 0, 0]
        expected = [0x83, 1, 0x02, 2, 3, 0xFF, 0xFF]
        self._process(input, expected)

    def testTrailingZeroValuesAreOmittedDiscrete(self):
        input = [1, 1, 1, 2, 3, 3, 3, 0]
        expected = [0x83, 1, 0x01, 2, 0x83, 3, 0xFF, 0xFF]
        self._process(input, expected)
        input = [1, 1, 1, 2, 3, 3, 3, 2, 1, 0]
        expected = [0x83, 1, 0x01, 2, 0x83, 3, 0x02, 2, 1, 0xFF, 0xFF]
        self._process(input, expected)
