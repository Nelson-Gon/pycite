import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import tempfile 
import bs4

from . import ncbi, pubmed, sciencedirect
import time

import logging

log_filename = "pycite_log.log"

log_format = "%(asctime)s %(levelname)s %(message)s"

log_level = logging.DEBUG

logging.basicConfig(filename = log_filename, 
        # Only showing time and actual message, other things like func name 
        # filename probably less useful for a user but may be useful for a 
        # developer
        format = log_format,
        filemode = "w"
        )

logger = logging.getLogger(__name__)


# Set logger to DEBUG so we get as much info in the log file as possible.
logger.setLevel(log_level)

# Use as access date (can be manually changed)
date_today = time.strftime("%d/%b/%Y")


def match_source(input_line):
    return re.findall("pubmed|ncbi|jstor|sciencedirect", input_line)


def switch_method(input_line, input_file, output_file, cit_list, bs4_link, **kwargs):
    # Write a dict to get the relevant method, do this only once.
    # This avoids writing several nested if statements and is probably easier to debug/refactor
    methods = {"pubmed": pubmed.pubmed_final_citation,
               "ncbi": ncbi.ncbi_final_citation,
               "sciencedirect": sciencedirect.sd_final_citation}
            #    "jstor": jstor.jstor_citation}

    use_method = match_source(input_line)[0]

    # The above should throw an index error but for whatever reason it does not with []
    actual_method = methods[use_method](bs4_link, **kwargs) if use_method == "pubmed" else methods[use_method](bs4_link)
    # Only get a method if it exists
    # if not use_method:
    #  warn (f"No suitable method found for {input_line},skipping....")
    if use_method in methods.keys():
        # Can directly send to logger but for now do it manually 
        logger.info(f"{input_line} in {input_file.name} is a(n) {use_method} link, using {use_method} methods")
        # output_file.write(f"{actual_method}\n") We write to the output file in the cite method now
        # The switch method now only creates a list with all the citations
        # Add date accessed
        cit_list.append(actual_method + " [Accessed " + date_today + "]")


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

        # Assert file existence
        for _file in [self.input_file, self.output_file]:

            try:
                assert os.path.isfile(_file), f"{_file} does not exist"
            except AssertionError:
                # Perhaps check for specific OS Errors eg not a file error, etc?
                # Using an assertion error seems simple but may be less specific.
                logger.error(f"{_file} does not exist")
                raise FileNotFoundError(f"{_file} does not exist")
            else:
                # Get format of file, for now only support txt files
                file_format = re.findall("\\.(\\w+)", _file)
                if file_format:
                    file_format = file_format[0]
                    try:
                        assert file_format == "txt", f"Only txt files supported for now, not {file_format}"
                    except AssertionError:
                        logger.error(f"Only txt files supported for now, not {file_format}")
                        raise
                    else:
                        pass
                else:
                    logger.error(f"No file format was detected in {_file}, exiting..")
                    raise ValueError(f"No file format was detected in {_file}, exiting...")

    def cite(self):
        final_citations = []
        # This is useful for tests (we use tempfile) to avoid permission denied errors, on Window$
        use_out_file = self.output_file if isinstance(self.output_file, 
                                tempfile._TemporaryFileWrapper) else open(self.output_file, "w")
        with open(self.input_file, "r") as in_file, use_out_file as out_file:
            for line in in_file:
                # Assume that links are inputted as lines in the input file

                try:
                    # Running curl works but not requests, no idea why
                    # curl -I "https://www.jstor.org/stable/26469531" --user-agent "Mozilla/5.0"
                    use_agent = {'User-Agent': 'Mozilla/5.0'} if "jstor" in line else {'User-Agent': 'XYZ/3.0'}
                    paper_link = urlopen(Request(line, headers=use_agent))
                    # TODO: Jstor citations work locally but not remote, temporarily disabling jstor tests.
                    # match_source(line)[0]
                except HTTPError as err:
                    logger.error(f"{line} not reachable, code: {str(err.code)}")
                    raise ValueError(f"{line} not reachable, code: {str(err.code)}")
                except URLError as err:
                    logger.error(f"{line} not reachable, reason {str(err.reason)}")
                    raise ValueError(f"{line} not reachable, reason: {str(err.reason)}")
                else:
                    # Convert to a BS4 object
                    bs4_link = bs4.BeautifulSoup(paper_link, features="html.parser")
                    switch_method(line, in_file, out_file, final_citations, bs4_link, show_doi=self.show_doi)
                    continue
            final_citations.sort()  # Sorting the final citations list

            for cit in final_citations:
                # Writing the sorted citations to the output file.
                out_file.write(f"{cit}\n")
        return final_citations
