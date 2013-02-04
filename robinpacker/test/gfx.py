import array
import unittest

import robinpacker.packers.gfx

class TestGfxRleEncoder(unittest.TestCase):
    def setUp(self):
        class MockGfxData(object):
            def __init__(self):
                self.data = None
        self.gfx_data = MockGfxData()

#    def testScenarioOne(self):
#        self.gfx_data.data = array.array('B', [1, 1, 1, 2, 3, 4, 5, 5, 6, 0, 0, 0])
#        expected = array.array('B', [0x83, 1, 0x05, 2, 3, 4, 5, 5, 0x01, 6, 0xFF] )
#        result = robinpacker.packers.gfx.encodeGfx(self.gfx_data)
#        self.assertEqual(result, expected)

    def testRepeatingValues(self):
        self.gfx_data.data = array.array('B', [1, 1, 1])
        expected = array.array('B', [0x83, 1, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testManyRepeatingValues(self):
        self.gfx_data.data = array.array('B', [1] * 0x80)
        expected = array.array('B', [0xFF, 1, 0x81, 1, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testMultipleRepeatingValues(self):
        self.gfx_data.data = array.array('B', [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3])
        expected = array.array('B', [0x85, 1, 0x84, 2, 0x83, 3, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testDiscreteValues(self):
        self.gfx_data.data = array.array('B', [1, 2, 3])
        expected = array.array('B', [0x03, 1, 2, 3, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testManyDiscreteValues(self):
        self.gfx_data.data = array.array('B', [1, 2, 3] * 43)
        expected = array.array('B', [0x7F] + [1, 2, 3] * 42 + [1, 0x02, 2, 3, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testMultipleDiscreteValuesWithRepeatingValuesInTheMiddle(self):
        self.gfx_data.data = array.array('B', [1, 2, 3, 4, 4, 4, 5, 6, 7])
        expected = array.array('B', [0x03, 1, 2, 3, 0x83, 4, 0x03, 5, 6, 7, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)

    def testMultipleRepeatingValuesWithDiscreteValuesInTheMiddle(self):
        self.gfx_data.data = array.array('B', [1, 1, 1, 2, 3, 4, 4, 4, 4])
        expected = array.array('B', [0x83, 1, 0x02, 2, 3, 0x84, 4, 0xFF] )
        encoder = robinpacker.packers.gfx.GfxRleEncoder()
        result = encoder.encodeGfx(self.gfx_data)
        self.assertEqual(result, expected)
