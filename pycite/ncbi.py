"""
Author: Nelson Gonzabato
Free Open Source Software, free and always will be.
"""
import re
from .helpers import remove_newlines, split_authors


# Citation methods for NCBI based addresses

def ncbi_title(bs4_object):
    title = bs4_object.find_all("h1", {"class": "content-title"})[0].text
    return title


def ncbi_journal_volume_year(bs4_object):
    journal_volumes = bs4_object.find_all("a", {"class": "navlink"})
    # Find Journal Name
    journal = journal_volumes[1].text
    # Find journal volume and year
    volume_year = journal_volumes[2].text
    vol_yr_split = re.split(";", volume_year)
    # index to remove the "v" from volumes
    volume = vol_yr_split[0][2:]
    # year
    year = re.sub("\\D", "", vol_yr_split[1])
    return journal, volume, year


def ncbi_page_numbers(bs4_object):
    # Pages
    # Split along a colon, the result is the page number
    # -1 to get the last result in the list returned
    page_numbers = re.split(":", bs4_object.find_all("div", {"class": "part1"})[0].text)[-1]
    page_numbers = remove_newlines(page_numbers)
    return page_numbers


def ncbi_authors(bs4_object):
    # Find the authors tag
    authors = bs4_object.find_all("div", {'class': 'contrib-group fm-author'})[0].text
    # Sanitize authors list
    authors_list = re.sub("[\\d*]", "", authors)
    authors_cleaner = re.sub(",(?=,)|,$", "", authors_list)
    # Split authors list
    authors_split = re.split(",", authors_cleaner)
    # Reverse author names, last first first last
    authors_split_clean = [re.sub("\\sand\\s", "",
                                  re.sub(r"(.*)(\\s)(.*)", "\\3\\2\\1", x)) for x in authors_split]

    # Merge these for now
    authors_split_clean[-1] = re.sub("(\\w.*)", "& \\1", authors_split_clean[-1])
    authors_split_clean[0] = re.sub("(\\w.*)", "\\1 ", authors_split_clean[0])
    authors_final = ",".join(authors_split_clean)
    # Clean authors further
    # TODO: This adds unnecessary steps, need to reduce this
    authors_final = ", ".join(split_authors(authors_final))
    return authors_final


def ncbi_final_citation(bs4_object):
    # Harvard Style
    # Authors (Year) Title, journal, Volume, pages
    # TODO: Make italics
    # TODO: Add DOIs in NCBI
    combined_citation = (ncbi_authors(bs4_object)
                         + " (" + ncbi_journal_volume_year(bs4_object)[2]
                         + ") " + " " + ncbi_title(bs4_object)
                         + " " + ncbi_journal_volume_year(bs4_object)[0]
                         + ", " + ncbi_journal_volume_year(bs4_object)[1]
                         + ", " + ncbi_page_numbers(bs4_object))
    return combined_citation
