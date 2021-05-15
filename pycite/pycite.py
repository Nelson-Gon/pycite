import bs4
from urllib.request import urlopen, Request
import re


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
