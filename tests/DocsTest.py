from __future__ import unicode_literals

import unittest
from builtins import str

from tidylib import tidy_document

DOC = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title></title>
  </head>
  <body>
    %s
  </body>
</html>
'''


class TestDocs1(unittest.TestCase):
    """ Test some sample documents """
    def test_doc_with_unclosed_tag(self):
        h = "<p>hello"
        expected = DOC % '''<p>
      hello
    </p>'''
        doc, err = tidy_document(h)
        self.assertEqual(doc, expected)
        
    def test_doc_with_incomplete_img_tag(self):
        h = "<img src='foo'>"
        expected = DOC % '''<img src='foo' alt="" />'''
        doc, err = tidy_document(h)
        self.assertEqual(doc, expected)
        
    def test_doc_with_entity(self):
        h = "&eacute;"
        expected = DOC % "&eacute;"
        doc, err = tidy_document(h)
        self.assertEqual(doc, expected)
        
        expected = DOC % "&#233;"
        doc, err = tidy_document(h, {'numeric-entities':1})
        self.assertEqual(doc, expected)
    
    def test_doc_with_unicode(self):
        h = "unicode string ß"
        expected = unicode(DOC, 'utf-8') % h
        doc, err = tidy_document(h)
        self.assertEqual(doc, expected)
        
    def test_doc_with_unicode_subclass(self):
        class MyUnicode(str):
            pass
        
        h = MyUnicode("unicode string ß")
        expected = str(DOC, 'utf-8') % h
        doc, err = tidy_document(h)
        self.assertEqual(doc, expected)
        
    
if __name__ == '__main__':
    unittest.main()