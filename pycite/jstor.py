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

def jstor_title(bs4_object):
    return remove_newlines(bs4_object.find_all("pharos-heading")[0].text)

def jstor_volume_issue_page(bs4_object):
    vol_issue_pages = bs4_object.find_all("div", {"class": "columns"})[1].find_all("div")[1].text
    vol_iss_pg = re.sub("\([^)]*\)|[Vol. No. pp.\s]", "", vol_issue_pages)
    return re.sub("(.*,)(.*)(,.*)", "\\1 (\\2) \\3", vol_iss_pg)




