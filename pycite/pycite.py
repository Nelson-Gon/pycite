import bs4
from urllib.request import urlopen, Request
import re


# Use a set to ensure that we do not have duplicate names in there
def pubmed_authors(bs4_object, target_class="full-name"):
    """
    :param bs4_object: An object of class Beautiful Soup
    :param target_class: Target class where the authors are found.
    :return: Pubmed authors, abbreviated.
    """
    res = bs4_object.find_all("a", {'class': target_class})
    res_no_dupes = res[:len(res) // 2]
    authors = [x.text for x in res_no_dupes]
    authors_final = []
    for author in authors:
        # Split by space
        authors_split = re.split("\\s", author)
        # Reverse author names, last first first last
        authors_reverse = authors_split[::-1]
        authors_reverse[1:] = [x[0] for x in authors_reverse[1:]]
        # Join with a space
        authors_joined = " ".join(authors_reverse)
        authors_final.append(authors_joined)

    # TODO: Make last author appear with the & instead of a comma
    # TODO: Make middle name last in the abbreviations?

    return ", ".join(authors_final)


def remove_newlines(in_str):
    """
    :param in_str: Remove new lines and unwanted spaces
    :return: A cleaner string
    """

    return re.sub("\\n|\\s{2,}", "", in_str)


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


def pubmed_year_volume_pages(bs4_object):
    """
    :param bs4_object: An object created with bs4's BeautifulSoup
    :return: A tuple containing the year, volume, and page numbers
    """
    dates_vol_pages = re.split(":|;", bs4_object.find_all("span", {'class': 'cit'})[0].text)
    year = re.split(" ", dates_vol_pages[0])[0]
    return year
    # if len(dates_vol_pages) == 1:
    #     return res
    # elif len(dates_vol_pages) == 2:
    #     return res + dates_vol_pages[1]
    # else:
    #     return res + dates_vol_pages[1] + dates_vol_pages[2]


def pubmed_final_citation(bs4_object):
    """
    :param bs4_object: An object of class BeautifulSoup
    :return: A pubmed specific citation
    """
    # TODO: Figure out how to solve issues with inconsistent lengths of yr_vol_page
    # return only years for now
    final_citation = pubmed_authors(bs4_object) + " " + pubmed_title(bs4_object) + " (" + \
                     pubmed_year_volume_pages(bs4_object) + ") " + pubmed_journal(bs4_object)
    # + ", " + pubmed_year_volume_pages(bs4_object)[1] + ", " + \
    # pubmed_year_volume_pages(bs4_object)[2]
    return final_citation


def split_authors(authors_list):
    """
    :param authors_list A list of authors to further split
    :return A cleaner version of the authors list
    """

    test_split = re.split(",", authors_list)
    splits = [re.split(" ", x) for x in test_split]
    final_authors = []
    for authors in splits:
        # Remove empty splits
        authors_split = list(filter(None, authors))
        # Abbreviate anything except the last name
        split_at = 1 if len(authors_split) <= 2 else 2
        authors_split[split_at:] = [x[:1] for x in authors_split[split_at:]]
        final_authors.append(" ".join(authors_split))
    return final_authors


class PyCite(object):
    def __init__(self, links_file):
        """
        :param links_file A file containing links to papers to cite
        :return An object of class pycite
        """
        self.links_file = links_file

    def cite(self):
        final_citations = []
        with open(self.links_file, "r") as links_file:
            for line in links_file:
                print(f"Now citing {line} found in {links_file.name}")
                # Assume that links are inputted as lines in the input file
                paper_link = urlopen(Request(line, headers={'User-Agent': 'XYZ/3.0'}))
                # Convert to a BS4 object
                bs4_link = bs4.BeautifulSoup(paper_link, features="html.parser")
                if "pubmed" in line:
                    print(f"{line} looks like a pubmed link, using pubmed methods...")
                    final_citations.append(pubmed_final_citation(bs4_link))
                    continue
                # Find title
                title = bs4_link.find_all("h1", {"class": "content-title"})[0].text
                journal_volumes = bs4_link.find_all("a", {"class": "navlink"})
                # Find Journal Name
                journal = journal_volumes[1].text
                # Find journal volume and year
                volume_year = journal_volumes[2].text
                vol_yr_split = re.split(";", volume_year)
                # index to remove the "v" from volumes
                volume = vol_yr_split[0][2:]
                # year
                year = re.sub(r"\D", "", vol_yr_split[1])

                # Find the authors tag
                authors = bs4_link.find_all("div", {'class': 'contrib-group fm-author'})[0].text
                # Sanitize authors list
                authors_list = re.sub(r"[\d*]", "", authors)
                authors_cleaner = re.sub(",(?=,)|,$", "", authors_list)
                # Split authors list
                authors_split = re.split(",", authors_cleaner)
                # Reverse author names, last first first last
                authors_split_clean = [re.sub(r"\sand\s", "",
                                              re.sub(r"(.*)(\s)(.*)", "\\3\\2\\1", x)) for x in authors_split]

                # Merge these for now
                authors_split_clean[-1] = re.sub(r"(\w.*)", "& \\1", authors_split_clean[-1])
                authors_split_clean[0] = re.sub(r"(\w.*)", "\\1 ", authors_split_clean[0])
                authors_final = ",".join(authors_split_clean)
                # Clean authors further
                # TODO: This adds unnecessary steps, need to reduce this
                authors_final = ",".join(split_authors(authors_final))

                # Harvard Style
                # Authors (Year) Title, journal, Volume, pages
                # TODO: Add page numbers
                # TODO: Make italics
                final_citations.append(authors_final + " " + title + " (" + year + ") " + journal + ", " + volume)
        return final_citations
