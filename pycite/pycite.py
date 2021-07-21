import bs4
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from . import ncbi, pubmed, sciencedirect, jstor
import re
import os





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
                raise FileNotFoundError(f"{_file} does not exist")
            else:
                # Get format of file, for now only support txt files
                file_format = re.findall("\\.(\\w+)", _file)
                if file_format:
                    file_format = file_format[0]
                    try:
                        assert file_format == "txt", f"Only txt files supported for now, not {file_format}"
                    except AssertionError:
                        raise
                    else:
                        pass
                else:
                    raise ValueError(f"No file format was detected in {_file}, exiting...")




    def cite(self):
        final_citations = []
        with open(self.input_file, "r") as in_file, open(self.output_file, "w") as out_file:
            for line in in_file:
                # Assume that links are inputted as lines in the input file
                try:
                    use_agent = {'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                    'like Gecko) Chrome/91.0.4472.164 Safari/537.36'} if "jstor" in line else {'User-Agent': 'XYZ/3.0'}
                    paper_link = urlopen(Request(line, headers=use_agent))
                except HTTPError as err:
                    raise ValueError(f"{line} not reachable, code: {str(err.code)}")
                except URLError as err:
                    raise ValueError(f"{line} not reachable, reason: {str(err.reason)}")
                else:
                    # Convert to a BS4 object
                    bs4_link = bs4.BeautifulSoup(paper_link, features="html.parser")
                    if "pubmed" in line:
                        print(f"{line} in {in_file.name} looks like a pubmed link, using pubmed methods...")
                        out_file.write(f"{pubmed.pubmed_final_citation(bs4_link,show_doi=self.show_doi)}\n")
                        final_citations.append(pubmed.pubmed_final_citation(bs4_link,show_doi=self.show_doi))
                        continue
                    if "ncbi" in line:
                        print(f"{line} in {in_file.name} looks like NCBI to me...")
                        out_file.write(f"{ncbi.ncbi_final_citation(bs4_link)}\n")
                        final_citations.append(ncbi.ncbi_final_citation(bs4_link))
                        continue
                        # TODO: Avoid repetition, use a single method to call the relevant methods e.g. a dict?
                    if "sciencedirect" in line:
                        print(f"{line} in {in_file.name} looks like Science Direct to me...")
                        out_file.write(f"{sciencedirect.sd_final_citation(bs4_link)}\n")
                        final_citations.append(sciencedirect.sd_final_citation(bs4_link))
                        continue
                    if "jstor" in line:
                        print(f"{line} in {in_file.name} is a JSTOR link, using jstor methods")
                        out_file.write(f"{jstor.jstor_citation(bs4_link)}\n")
                        final_citations.append(jstor.jstor_citation(bs4_link))
                        continue



        return final_citations


