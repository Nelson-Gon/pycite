import bs4
import re


def sd_title(bs4_object, target={"class":"title-text"}):
    """

    :param bs4_object: An object of class BeautifulSoup
    :param target: Target HTML tag. Defaults to class:title-text, a dict.
    :return: Returns paper title from Science Direct
    """

    return bs4_object.find_all("span",target)[0].text



def sd_authors(bs4_object):
    """

    :param bs4_object: An object of class BeautifulSoup
    :return: Authors list
    """
    # Authors are listed separately on the site at this time i.e given alone
    # and last alone
    sd_given = bs4_object.find_all("span", {"class": "given-name"})
    given_names = [x.text for x in sd_given]
    # Last names
    sd_last = bs4_object.find_all("span", {"class": "surname"})
    surnames = [x.text for x in sd_last]
    # Next abbreviate and combine with respective surnames
    # First need to split along a space wherever it appears
    given_split = [[y[0] for y in x.split()] for x in given_names]
    # Join as single string
    given_joined = ["".join(x) for x in given_split]
    # Combine surname plus last name
    # TODO: Assert that lengths of surnames and given are equal
    authors_list = list(map(lambda x, y: x + " " + y, surnames, given_joined))
    # Make last appear with &
    authors_list[len(authors_list) - 1] = "& " + authors_list[len(authors_list) - 1]
    return ",".join(authors_list)

def sd_vol_year_pages(bs4_object, target={"class": "text-xs"}):
    """

    :param bs4_object: An object of class BeautifulSoup
    :param target: A dict specifying the target HTML tag
    :return: Volume, Year, Pages
    """

    vol_year_pages = bs4_object.find_all("div", target)[0].text
    # Volume, issue, date including year d/sm/sy, pages
    # Split along comma
    vol_year_pages_split = vol_year_pages.split(",")
    # Volume: Remove the word Volume
    volume = re.sub("\D","",vol_year_pages_split[0])
    issue = re.sub("\D","",vol_year_pages_split[1])
    # If DMY, split along a space, whatever comes last is the year
    # TODO: Assert that year lengths is 2
    year = vol_year_pages_split[2].split()[-1]
    # TODO: This seems so forced, need to be more precise in removing non digits
    pages = re.sub(" Pages ", "", vol_year_pages_split[-1])
    return volume, issue, year, pages

def sd_journal_name(bs4_object):
    """

    :param bs4_object: An object of class BeautifulSoup
    :return: Journal Name
    """
    return bs4_object.find_all("a", {"class":"publication-title-link"})[0].text


def sd_final_citation(bs4_object):
    """

    :param bs4_object: An object of class BeautifulSoup
    :return: Final citation of a science direct paper.
    """

    combined = (sd_authors(bs4_object) + " " + "(" + sd_vol_year_pages(bs4_object)[2]  + ") "
                + sd_title(bs4_object) + ". " + sd_journal_name(bs4_object) + ", " + sd_vol_year_pages(bs4_object)[0]
                + "(" + sd_vol_year_pages(bs4_object)[1] + "), " + sd_vol_year_pages(bs4_object)[3])
    return combined









