"""
Python Citations Generator
Author: Nelson Gonzabato
Free Open Source Software.
Free, and always will be.
Made with Love.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from version import __version__
__author__ = "Nelson Gonzabato"
__all__ = ["pycite"]
assert isinstance(__version__, str)
__version__ = __version__

