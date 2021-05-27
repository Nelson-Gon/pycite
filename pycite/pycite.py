import bs4
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
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
    vols_pg_nos = list(filter(None,[re.findall("\\d+\\(.*\\):\\d+-\\d+", x) for x in dates_vol_pages]))
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
        final_volume_year_page = final_volume_year_page +  (volume, page_numbers)

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
    final_citation = (pubmed_authors(bs4_object) + " " + pubmed_title(bs4_object) + " (" +
                      year + ") " + pubmed_journal(bs4_object))
    if len(yrs_vols_pages) == 4:
        final_citation = final_citation + ", " + yrs_vols_pages[2] + ", " + yrs_vols_pages[3]
    if show_doi:
        final_citation = final_citation + " " + yrs_vols_pages[1]

    return final_citation


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
    year = re.sub(r"\D", "", vol_yr_split[1])
    return journal, volume, year

def ncbi_page_numbers(bs4_object):
    # Pages
    # Split along a colon, the result is the page number
    # -1 to get the last result in the list returned
    page_numbers = re.split(":", bs4_object.find_all("div", {"class": "part1"})[0].text)[-1]
    page_numbers = remove_newlines(page_numbers)
    return page_numbers

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

def ncbi_authors(bs4_object):
    # Find the authors tag
    authors = bs4_object.find_all("div", {'class': 'contrib-group fm-author'})[0].text
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
    return authors_final

def ncbi_final_citation(bs4_object):
    # Harvard Style
    # Authors (Year) Title, journal, Volume, pages
    # TODO: Make italics
    # TODO: Add DOIs in NCBI
    combined_citation = (ncbi_authors(bs4_object) + " " + ncbi_title(bs4_object)
                             + " (" + ncbi_journal_volume_year(bs4_object)[2]
                             + ") " + ncbi_journal_volume_year(bs4_object)[0]
                             + ", " + ncbi_journal_volume_year(bs4_object)[1]
                             + ", " + ncbi_page_numbers(bs4_object))
    return combined_citation



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
                # Assume that links are inputted as lines in the input file
                try:
                    paper_link = urlopen(Request(line, headers={'User-Agent': 'XYZ/3.0'}))
                except HTTPError as err:
                    raise ValueError(f"{line} not reachable, code: {str(err.code)}")
                except URLError as err:
                    raise ValueError(f"{line} not reachable, reason: {str(err.reason)}")
                else:
                    # Convert to a BS4 object
                    bs4_link = bs4.BeautifulSoup(paper_link, features="html.parser")
                    if "pubmed" in line:
                        print(f"{line} in {in_file.name} looks like a pubmed link, using pubmed methods...")
                        out_file.write(f"{pubmed_final_citation(bs4_link,show_doi=self.show_doi)}\n")
                        final_citations.append(pubmed_final_citation(bs4_link,show_doi=self.show_doi))
                        continue
                    if "ncbi" in line:
                        print(f"{line} in {in_file.name} looks like NCBI to me...")
                        out_file.write(f"{ncbi_final_citation(bs4_link)}\n")
                        final_citations.append(ncbi_final_citation(bs4_link))
                        continue

        return final_citations


