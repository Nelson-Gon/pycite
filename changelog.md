# pycite's changelog 

**pycite 0.1.3**

* Tests now rely on 

* JSTOR citations are no longer supported. 

* Fixed issues with NCBI citations not reversing author names. 

* Citations now include a date accessed attribute. 

* Citations now alphabetically as expected by Harvard citation standards. 

* Optimised imports, refactored to ensure that default arguments are immutable. RegEx matching now uses string literals 
as per PEP requirements.

* Updated documentation to include the author's contact details, if needed.   

**pycite 0.1.2**

* Refactored code that selects relevant methods to follow the DRY principle. 

* Fixed issues with titles appearing before years in citations. 

* Fixed issues with single JSTOR authors being truncated. See [#15](https://github.com/Nelson-Gon/pycite/issues/15).
  
* Now supporting JSTOR as a paper source. See [#15](https://github.com/Nelson-Gon/pycite/issues/15).

* Fixed issues with misplaced "&" in citations. See [#8](https://github.com/Nelson-Gon/pycite/issues/8).

* Fixed issues with mix up of science direct volumes, years, pages. See [#7](https://github.com/Nelson-Gon/pycite/issues/7). 

* Initial support for Science Direct papers. See [#6](https://github.com/Nelson-Gon/pycite/issues/6).  

* New modules `ncbi`, `helpers`, and `pubmed` can be imported with ambiguous `*` imports. 

* Introduced new modules "helpers", "ncbi", and "pubmed" to allow for some order and ensure we do not have a 
super long single file package. This really is to keep things tidy. 

* Extended tests to ensure that we raise custom exceptions as necessary.  

* NCBI citations now include page numbers.
* Script mode now has an optional `show_doi` argument to control DOI additions to PubMed citations. 
* PUbMed citations now include page numbers, where applicable. See https://github.com/Nelson-Gon/pycite/issues/2

* For PubMed citations, an optional `show_doi` argument was added to control whether dois should exist in the citation.

* Initial support for a script mode. 

**pycite 0.1.1**

* Fixed issues with inconsistent tuple lengths in Pubmed citations https://github.com/Nelson-Gon/pycite/issues/2

* `PyCite` now takes an `input_file` and `output_file` as arguments. 

* Fixed issues with incorrect author formatting for NCBI and Pubmed articles

* Initial support for Pubmed citations i.e., links in the form https://pubmed.ncbi.nlm.nih.gov/ 

* Explicitly set an HTML parser 

* Initial tests 

* Volumes no longer have the leading "v" attached. 

* Added `split_authors` a simple method to clean and abbreviate author names. 

* Fixed issues with actions not running on GitHub.

* Updated documentation 

**pycite 0.1.0**

* Initial release 
