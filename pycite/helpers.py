# Helper intermediate functions to clean up citations
# TODO: Keep these only wherever they are needed.
import re

def remove_newlines(in_str):
    """
    :param in_str: Remove new lines and unwanted spaces
    :return: A cleaner string
    """

    return re.sub("\\n|\\s{2,}", "", in_str)

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