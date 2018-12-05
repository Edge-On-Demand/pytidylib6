from __future__ import unicode_literals

import unittest
from builtins import str

from tidylib import tidy_fragment


class TestFrags1(unittest.TestCase):
    """ Test some sample fragment documents """
    def test_frag_with_unclosed_tag(self):
        h = "<p>hello"
        expected = '''<p>
      hello
    </p>'''
        doc, err = tidy_fragment(h)
        self.assertEqual(doc, expected)
        
    def test_frag_with_incomplete_img_tag(self):
        h = "<img src='foo'>"
        expected = '''<img src='foo' alt="" />'''
        doc, err = tidy_fragment(h)
        self.assertEqual(doc, expected)
        
    def test_frag_with_entity(self):
        h = "&eacute;"
        expected = "&eacute;"
        doc, err = tidy_fragment(h)
        self.assertEqual(doc, expected)
        
        expected = "&#233;"
        doc, err = tidy_fragment(h, {'numeric-entities':1})
        self.assertEqual(doc, expected)
    
    def test_frag_with_unicode(self):
        h = "unicode string ß"
        expected = h
        doc, err = tidy_fragment(h)
        self.assertEqual(doc, expected)

    def test_frag_with_unicode_subclass(self):
        class MyUnicode(str):
            pass

        h = MyUnicode("unicode string ß")
        expected = h
        doc, err = tidy_fragment(h)
        self.assertEqual(doc, expected)


if __name__ == '__main__':
    unittest.main()
