import bs4
from urllib.request import urlopen, Request
import re


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
    for author in authors:
        author_name = author.split()
        last_name = [author_name[len(author_name) - 1]]
        author_name = last_name + author_name[:len(author_name) - 1]
        authors_list.append(' '.join(author_name))

    authors_list = split_authors(', '.join(authors_list))
    authors = ', '.join(name for name in authors_list)
    return authors


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


def pubmed_year_volume_pages(bs4_object, show_doi=False):
    """
    :param bs4_object: An object created with bs4's BeautifulSoup
    :param show_doi Boolean to control if DOIs should be included in citations. Defaults to False
    :return: A tuple containing the year, volume, and page numbers
    """
    # Split only along ; since we can already obtain the DOI elsewhere.
    dates_vol_pages = re.split("[;]", bs4_object.find_all("span", {'class': 'cit'})[0].text)
    # Split year in the form Y M D along a space, year comes first
    year = re.split(" ", dates_vol_pages[0])[0]
    # doi +/ s.*
    paper_identity = bs4_object.find_all("span", {"class": "citation-doi"})[0].text
    # no_doi = re.sub(".*/(?=[Ss])", "", paper_identity.split()[1])

    return year, remove_newlines(paper_identity) if show_doi else year


def pubmed_final_citation(bs4_object, show_doi=False):
    """
    :param bs4_object: An object of class BeautifulSoup
    :param show_doi Boolean to control if DOIs should be included in citations. Defaults to False
    :return: A pubmed specific citation
    """
    # TODO: Add page numbers where applicable
    yrs_vols_pages = pubmed_year_volume_pages(bs4_object, show_doi=show_doi)
    # For some reason, year is returned as a tuple with dupes so
    # Need to get the year "twice" here again
    year = yrs_vols_pages[0] if show_doi else yrs_vols_pages[0][0]
    final_citation = (pubmed_authors(bs4_object) + " " + pubmed_title(bs4_object) + " (" +
                      year + ") " + pubmed_journal(bs4_object))
    if show_doi:
        final_citation = final_citation + " " + yrs_vols_pages[1]

    return final_citation


def split_authors(authors_list):
    """
    :param authors_list A list of authors to further split
    :return A cleaner version of the authors list
    """
    test_split = re.split(",", authors_list)
    # Remove 'and' or & symbol from the last author if it exists
    splits = [re.split("and |& | ", x) for x in test_split]
    final_authors = []

    for authors in splits:
        # Remove empty splits
        authors_split = list(filter(None, authors))
        # Abbreviate anything except the last name
        last_name = 0
        first_name = 1
        authors_split = [authors_split[last_name]] + [''.join([x[:first_name] for x in authors_split[first_name:]])]
        final_authors.append(" ".join(authors_split))

    # Make last author appear with the & symbol
    final_authors[len(final_authors) - 1] = "& " + final_authors[len(final_authors) - 1]
    return final_authors


class PyCite(object):
    def __init__(self, input_file, output_file, show_doi=False):
        """
        :param input_file A file containing links to papers to cite.
        :param output_file A file/filename to write citations to.
        :param show_doi Boolean to control if DOIs should be included in citations. Defaults to False.
        :return An object of class PyCite
        """
        self.input_file = input_file
        self.output_file = output_file
        self.show_doi = show_doi

    def cite(self):
        final_citations = []
        with open(self.input_file, "r") as in_file, open(self.output_file, "w") as out_file:
            for line in in_file:
                print(f"Now citing {line} found in {in_file.name}")
                # Assume that links are inputted as lines in the input file
                paper_link = urlopen(Request(line, headers={'User-Agent': 'XYZ/3.0'}))
                # Convert to a BS4 object
                bs4_link = bs4.BeautifulSoup(paper_link, features="html.parser")
                if "pubmed" in line:
                    print(f"{line} looks like a pubmed link, using pubmed methods...")
                    out_file.write(f"{pubmed_final_citation(bs4_link,show_doi=self.show_doi)}\n")
                    final_citations.append(pubmed_final_citation(bs4_link,show_doi=self.show_doi))
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
                authors_final = ", ".join(split_authors(authors_final))

                # Harvard Style
                # Authors (Year) Title, journal, Volume, pages
                # TODO: Add page numbers
                # TODO: Make italics
                combined_citation = authors_final + " " + title + " (" + year + ") " + journal + ", " + volume
                out_file.write(f"{combined_citation}\n")
                final_citations.append(combined_citation)
        return final_citations
