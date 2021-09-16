"""
Author: Nelson Gonzabato
Free Open Source Software, free and always will be.
"""
# Citation builders for PubMed
from .helpers import split_authors, remove_newlines
import re


def make_first_last(authors_list, save_to):
    """

    :param authors_list: A list of authors whose names should be reversed
    :param save_to: A list to save reversed authors to
    :return: Authors list reversed
    """
    for author in authors_list:
        author_name = author.split()
        last_name = [author_name[len(author_name) - 1]]
        author_name = last_name + author_name[:len(author_name) - 1]
        save_to.append(' '.join(author_name))


def pubmed_authors(bs4_object, target_class="full-name"):
    """
    :param bs4_object: An object of class Beautiful Soup
    :param target_class: Target class where the authors are found.
    :return: Pubmed authors, abbreviated.
    """
    res = bs4_object.find_all("a", {'class': target_class})
    # Delete duplicate entries
    res_no_dupes = res[:len(res) // 2]
    authors = [x.text for x in res_no_dupes]
    authors_list = []

    # Place last name in the front for each author
    make_first_last(authors, authors_list)

    authors_list = split_authors(', '.join(authors_list))
    authors = ', '.join(name for name in authors_list)
    return authors


def pubmed_title(bs4_object):
    """
    :param bs4_object: An object of class Beautiful soup
    :return: A pubmed journal article
    """
    return remove_newlines(bs4_object.find_all("h1", {"class": "heading-title"})[1].text)


def pubmed_journal(bs4_object):
    """
    :param bs4_object: An object of class BeautifulSoup
    :return: pubmed journal name
    """
    return remove_newlines(bs4_object.find_all("button",
                                               {'class': 'journal-actions-trigger'})[0].text)


def pubmed_year_volume_pages(bs4_object, show_doi=False):
    """
    :param bs4_object:
    :param show_doi: Boolean to control if DOIs should be included in citations. Defaults to False
    :return: A tuple containing the year, volume, and page numbers
    """

    # Split only along ; since we can already obtain the DOI elsewhere.
    dates_vol_pages = re.split("[;]", bs4_object.find_all("span", {'class': 'cit'})[0].text)
    # Split year in the form Y M D along a space, year comes first
    year = re.split(" ", dates_vol_pages[0])[0]
    # This finds volumes and page numbers if they exist
    # For example in https://pubmed.ncbi.nlm.nih.gov/18952168/
    # Volumes and page numbers exist as 18(6):756-64.
    vols_pg_nos = list(filter(None, [re.findall("\\d+\\(.*\\):\\d+-\\d+", x) for x in dates_vol_pages]))
    volume = None
    page_numbers = None
    if vols_pg_nos:
        # if vols_pgs_nos, then the first is the vol second page numbers
        vols_pg_nos = re.split(":", vols_pg_nos[0][0])
        volume = vols_pg_nos[0]
        page_numbers = vols_pg_nos[1]
    # doi +/ s.*
    paper_identity = bs4_object.find_all("span", {"class": "citation-doi"})[0].text
    # no_doi = re.sub(".*/(?=[Ss])", "", paper_identity.split()[1])

    final_volume_year_page = year, remove_newlines(paper_identity) if show_doi else year
    if volume:
        final_volume_year_page = final_volume_year_page + (volume, page_numbers)

    return final_volume_year_page


def pubmed_final_citation(bs4_object, show_doi=False):
    """
    :param bs4_object: An object of class BeautifulSoup
    :param show_doi: Boolean to control if DOIs should be included in citations. Defaults to False
    :return: A pubmed specific citation
    """
    yrs_vols_pages = pubmed_year_volume_pages(bs4_object, show_doi=show_doi)
    # For some reason, year is returned as a tuple with dupes so
    # Need to get the year "twice" here again
    year = yrs_vols_pages[0]
    final_citation = (pubmed_authors(bs4_object) + " (" +
                      year + ") " + " " + pubmed_title(bs4_object) + " " + pubmed_journal(bs4_object))
    if len(yrs_vols_pages) == 4:
        final_citation = final_citation + ", " + yrs_vols_pages[2] + ", " + yrs_vols_pages[3]
    if show_doi:
        final_citation = final_citation + " " + yrs_vols_pages[1]

    return final_citation
