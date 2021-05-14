import bs4
from urllib.request import urlopen, Request
import re


# Open web url

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
                # Assume that links are inputed as lines in the input file
                paper_link = urlopen(Request(line, headers={'User-Agent': 'XYZ/3.0'}))
                # Convert to a BS4 object
                bs4_link = bs4.BeautifulSoup(paper_link)
                # Find title
                title = bs4_link.find_all("h1", {"class": "content-title"})[0].text
                # Find Journal Name
                journal = bs4_link.find_all("a", {"class": "navlink"})[1].text
                # Find journal volume and year
                volume_year = bs4_link.find_all("a", {"class": "navlink"})[2].text
                vol_yr_split = re.split(";", volume_year)
                volume = vol_yr_split[0]
                # year
                year = re.sub("\D", "", vol_yr_split[1])

                # Find the authors tag
                authors = bs4_link.find_all("div", {'class': 'contrib-group fm-author'})[0].text
                # Sanitize authors list
                authors_list = re.sub("[\d*]", "", authors)
                authors_cleaner = re.sub(",(?=,)|,$", "", authors_list)
                # Split authors list
                authors_split = re.split(",", authors_cleaner)
                # Reverse author names, last first first last
                authors_split_clean = [re.sub("\sand\s", "",
                                              re.sub("(.*)(\s)(.*)", "\\3\\2\\1", x)) for x in authors_split]

                # Merge these for now
                authors_split_clean[-1] = re.sub("(\w.*)", "& \\1", authors_split_clean[-1])
                authors_split_clean[0] = re.sub("(\w.*)", "\\1 ", authors_split_clean[0])
                authors_final = ",".join(authors_split_clean)

                # Harvard Style
                # Authors (Year) Title, journal, Volume, pages
                # TODO: Add page numbers
                # TODO: Make italics
                final_citations.append(authors_final + " " + title + " (" + year + ") " + journal + ", " + volume)
        return final_citations
