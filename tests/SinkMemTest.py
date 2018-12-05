import unittest

from tidylib import tidy_document, tidy_fragment, sink


class TestSinkMemory(unittest.TestCase):
    """ Make sure error sinks are cleared properly """
    
    def test_tidy_document(self):
        h = "<p>hello"
        for i in range(100):
            doc, err = tidy_document(h)
        self.assertEqual(sink.sinks, {})
        
    def test_tidy_fragment(self):
        h = "<p>hello"
        for i in range(100):
            doc, err = tidy_fragment(h)
        self.assertEqual(sink.sinks, {})


if __name__ == '__main__':
    unittest.main()
