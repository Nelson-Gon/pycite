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
non_existing_file = "notafile.txt"


class TestPyCite(unittest.TestCase):

    def test_pycite(self):
        # Create an object of class PyCite
        test_object = PyCite(in_file, out_file, show_doi=False)
        self.assertTrue(isinstance(test_object, PyCite))
        # Check that we have the expected number of citations
        citations = test_object.cite()
        self.assertEqual(len(citations), 9)
        print(citations)
        # Check that we can raise exceptions whenever necessary
        with self.assertRaises(ValueError) as err:
            test_nonsupported = PyCite(in_file_unsupported, out_file, show_doi=False)
            test_nonsupported.cite()
            # Expect an error to do with SSL certificate verification
            # Not the most ideal way as this exception may change in the future
            # TODO: Assertions for error codes from HTTPError instead of URLError
        self.assertTrue("certificate verify failed" in str(err.exception))
        # Check that non existing files throw an assertion error as expected
        with self.assertRaises(AssertionError) as err:
            non_valid_file_object = PyCite(non_existing_file,"notvalidttoo.txt",show_doi=False)
        self.assertEqual(str(err.exception), "notafile.txt does not exist")



if __name__ == "__main__":
    unittest.main()
