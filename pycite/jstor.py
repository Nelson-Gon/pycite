"""
Author: Nelson Gonzabato
Free Open Source Software, free and always will be.
"""
import re
from .helpers import remove_newlines, split_authors
from urllib.request import urlopen, Request
import bs4

def jstor_authors(bs4_object):
    authors = remove_newlines(bs4_object.find_all("div", {"class": "author-font"})[0].text)
    # Split authors by a comma
    authors_split=authors.split(",")
    # For each author, capture first and last names, reverse these
    first_last = [re.sub("(.*)(\s)(.*)", "\\3 \\1",authrs) for authrs in authors_split]

    return first_last

