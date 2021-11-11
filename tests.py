"""
pycite's unittests
Author: Nelson Gonzabato
Free Open Source Software
Free and always will be.
"""

import unittest
import os, sys
# from pycite.jstor import jstor_authors
from pycite.pycite import PyCite
from shutil import copytree, rmtree
import tempfile 

# Make paths to tests

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
# Create a temporary test file for citations 
out_file_temp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
out_file = out_file_temp.name 
# Would be better if we could specify the temporary file's directory 
# out_file = out_file = os.path.join(test_dir, "citations.txt")

# Create temporary directory to use for tests (?) 
# This is memory and time intensive but ensures that we avoid overwriting testfiles 
# tempfile.TemporaryDirectory fails for whatever reason
# print("Creating a temporary test directory") 
# copytree(test_dir, os.path.join(test_dir , "temp"))
# test_dir_temp = os.path.join(test_dir, "temp")


def create_test_object(in_file, out_f=out_file, **kwargs):
    return PyCite(input_file=os.path.join(test_dir,in_file), output_file=out_f, **kwargs)



class TestPyCite(unittest.TestCase):


    def test_instance_creation(self):
        self.assertIsInstance(create_test_object(in_file="testlinks.txt", show_doi=False), PyCite)

    def test_list_creation(self):
        # Check that we have two citation lists created 
        self.assertEqual(len(create_test_object(in_file="testlinks.txt", show_doi=False).cite()), 12)

    def test_exceptions(self):

        with self.assertRaises(FileNotFoundError) as err:
            create_test_object(in_file="notafile.txt", out_f="notvalidtoo.txt", show_doi=False)
        self.assertTrue("notafile.txt does not exist" in str(err.exception))

        # Check that we only have the expected file format, txt for now
        with self.assertRaises(AssertionError) as err:
            create_test_object(in_file="nottxt.pdf", out_f=out_file, show_doi=False)
        self.assertEqual(str(err.exception), "Only txt files supported for now, not pdf")

        # Check that if no file format exists, we raise a ValueError
        with self.assertRaises(ValueError) as err:
            create_test_object(in_file="nofileformat", out_f=out_file, show_doi=False)
        self.assertTrue("No file format was detected" in str(err.exception))

        # print(f"Removing temporary test file {out_file}")
        # out_file_temp.close()
        # os.unlink(out_file)
    
    # @unittest.skipIf("GITHUB_ACTIONS" in os.environ and os.environ["GITHUB_ACTIONS"],
    #                  "These tests are known to fail due to jstor github blocks")
    # def test_jstor(self):
    #     test_jstor = create_test_object("testjstor.txt")
    #     self.assertTrue(isinstance(test_jstor, PyCite))
    #     self.assertEqual(len(test_jstor.cite()), 2)
        


if __name__ == "__main__":
    unittest.main()
  

