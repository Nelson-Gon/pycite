"""
pycite's unittests
Author: Nelson Gonzabato
Free Open Source Software
Free and always will be.
"""

import unittest
import os
from pycite.pycite import PyCite

# Make paths to tests

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")

in_file = os.path.join(test_dir, "testlinks.txt")
out_file = os.path.join(test_dir, "citations.txt")
in_file_unsupported = os.path.join(test_dir, "unsupportedlinks.txt")
non_existing_file = os.path.join(test_dir,"notafile.txt")
not_txt = os.path.join(test_dir,"nottxt.pdf")
no_format = os.path.join(test_dir,"nofileformat")


class TestPyCite(unittest.TestCase):

    def test_pycite(self):
        # Create an object of class PyCite
        test_object = PyCite(in_file, out_file, show_doi=False)
        self.assertTrue(isinstance(test_object, PyCite))
        # Check that we have the expected number of citations
        citations = test_object.cite()
        self.assertEqual(len(citations), 14)
        print(citations)
        # Check that we can raise exceptions whenever necessary
        # with self.assertRaises(ValueError) as err:
        #     test_nonsupported = PyCite(in_file_unsupported, out_file, show_doi=False)
        #     test_nonsupported.cite()
        #     # Expect an error to do with SSL certificate verification
        #     # Not the most ideal way as this exception may change in the future
        # self.assertTrue("certificate verify failed" in str(err.exception))
        # Check that non existing files throw a FileNotFoundError for now
        with self.assertRaises(FileNotFoundError) as err:
            PyCite(non_existing_file,"notvalidttoo.txt",show_doi=False)
        self.assertTrue("notafile.txt does not exist" in str(err.exception))



        # Check that we only have the expected file format, txt for now
        with self.assertRaises(AssertionError) as err:
            not_txt_object = PyCite(not_txt, "nottxt.pdf")
        self.assertEqual(str(err.exception), "Only txt files supported for now, not pdf")

        # Check that if no file format exists, we raise a ValueError
        with self.assertRaises(ValueError) as err:
            no_file_format = PyCite(no_format, no_format)
        self.assertTrue("No file format was detected" in str(err.exception))



if __name__ == "__main__":
    unittest.main()
