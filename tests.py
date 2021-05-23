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


class TestPyCite(unittest.TestCase):

    def test_pycite(self):
        # Create an object of class PyCite
        test_object = PyCite(in_file, out_file, show_doi=False)
        self.assertTrue(isinstance(test_object, PyCite))
        # Check that we have the expected number of citations
        citations = test_object.cite()
        self.assertEqual(len(citations), 9)
        print(citations)


if __name__ == "__main__":
    unittest.main()
