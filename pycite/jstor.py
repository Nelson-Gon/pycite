"""
Author: Nelson Gonzabato
Free Open Source Software, free and always will be.
"""
import re
from .helpers import remove_newlines, split_authors


def jstor_authors(bs4_object):
    authors = remove_newlines(bs4_object.find_all("div", {"class": "author-font"})[0].text)
    authors = re.sub(" and ", ",", authors)
    return " ".join(split_authors(authors)) if "," in authors else authors


def jstor_title(bs4_object):
    return remove_newlines(bs4_object.find_all("pharos-heading")[0].text)


def jstor_volume_issue_page(bs4_object):
    vol_issue_pages = bs4_object.find_all("div", {"class": "columns"})[1].find_all("div")[1].text
    vol_iss_pg = re.sub(r"\([^)]*\)|Vol. No. pp.\s", "", vol_issue_pages)
    return re.sub(r"(.*)(,)(.*)(,.*)", "\\1 (\\3) \\4", vol_iss_pg)


def jstor_journal(bs4_object):
    return re.sub(r"^\s|\s$", "", bs4_object.find_all("div", {"class": "columns"})[1].find_all("div")[0].text)


def jstor_year(bs4_object):
    mon_year = re.search(r"\([^)]*\)", bs4_object.find_all("div", {"class": "columns"})[1].find_all("div")[1].text)
    # Get the last element in a ,/\s split
    # If split is a comma, replace it with a \\s
    mon_year = re.sub(",", " ", mon_year.group(0))
    year = re.sub(r"\D", "", mon_year.split(" ")[-1])
    return year


def jstor_citation(bs4_object):
    combined_citation = (jstor_authors(bs4_object) + " (" + jstor_year(bs4_object)
                         + ") " +
                         " " + jstor_title(bs4_object)
                         + jstor_journal(bs4_object) + ", " +
                         jstor_volume_issue_page(bs4_object))
    return combined_citation
