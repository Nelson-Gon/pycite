"""
pycite's unit tests
Author: Nelson Gonzabato
Free Open Source Software
Free and always will be.
"""
import pytest 
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
def make_file(file_name):
    return os.path.join(test_dir,file_name)
@pytest.fixture 
def test_object(in_file="testlinks.txt", out_f=out_file, **kwargs):
    return PyCite(input_file= make_file(in_file),output_file = out_f,
                show_doi=False, **kwargs)


# We could use a class and make use of pytest's unittest compatibility 
# but prefer to do it from scratch 


def test_instance_creation(test_object):
    assert isinstance(test_object, PyCite)

def test_list_creation(test_object):
    # Check that we have two citation lists created 
    assert len(test_object.cite()) == 12


# To pass arguments to a fixture, we need to parameterize 
# Using closures seems easier 

@pytest.mark.parametrize("in_file","expected", [(make_file("notafile.txt")), (FileNotFoundError)])
def test_missing_file(test_object, in_file, expected):
    with pytest.raises(FileNotFoundError) as err:
        test_object.cite()
        assert str(err) == "notafile.txt does not exist"

# While theoretically we could use dynamic variables with parametrize, it seems less convenient
@pytest.mark.parametrize("in_file","expected",  [(make_file("nottxt.pdf")), (AssertionError)])
def test_non_supported(test_object, in_file, expected):
    print(in_file)
    # Check that we only have the expected file format, txt for now
    with pytest.raises(AssertionError) as err:
        # We cannot use err.exception in pytest's raise context manager 
        test_object.cite()
        assert str(err) == "Only txt files supported for now, not pdf"

@pytest.mark.parametrize("in_file", "expected",  [(make_file("nofileformat")), (ValueError)])
def test_no_format(test_object, in_file, expected):
    # Check that if no file format exists, we raise a ValueError
    with pytest.raises(ValueError) as err:
        test_object.cite()
        assert "No file format was detected" == str(err)

        # print(f"Removing temporary test file {out_file}")
        # out_file_temp.close()
        # os.unlink(out_file)
    
    # @unittest.skipIf("GITHUB_ACTIONS" in os.environ and os.environ["GITHUB_ACTIONS"],
    #                  "These tests are known to fail due to jstor github blocks")
    # def test_jstor(self):
    #     test_jstor = create_test_object("testjstor.txt")
    #     self.assertTrue(isinstance(test_jstor, PyCite))
    #     self.assertEqual(len(test_jstor.cite()), 2)
    

  

