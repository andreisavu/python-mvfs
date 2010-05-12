
import os
import unittest
import tempfile
import magic

import mvfs.openers

class TestOpeners(unittest.TestCase):

    def setUp(self):
        _, self.filepath = tempfile.mkstemp()

        self.mime = magic.open(magic.MAGIC_MIME)
        self.mime.load()

    def tearDown(self):
        os.unlink(self.filepath)

    def check(self, op, expected_mime):
        with op.open(self.filepath, 'w') as f:
            f.write('a dummy text')
        self.assertEqual(self.mime.file(self.filepath), expected_mime)

    def test_plain_file_opener(self):
        self.check(mvfs.openers.PlainFileOpener(), 'text/plain; charset=us-ascii')

    def test_gzip_file_opener(self):
        self.check(mvfs.openers.GZipFileOpener(), 'application/x-gzip; charset=binary')
        
