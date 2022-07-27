# pycite: Python Citations Generator 


[![DOI](https://zenodo.org/badge/367264942.svg)](https://zenodo.org/badge/latestdoi/367264942)
[![PyPI version fury.io](https://badge.fury.io/py/pycite.svg)](https://pypi.python.org/pypi/pycite/)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active) 
[![Codecov](https://codecov.io/gh/Nelson-Gon/pycite/branch/main/graph/badge.svg)](https://codecov.io/gh/Nelson-Gon/pycite?branch=main)
![Test-Package](https://github.com/Nelson-Gon/pycite/workflows/Test-Package/badge.svg)
[![PyPI license](https://img.shields.io/pypi/l/pycite.svg)](https://pypi.python.org/pypi/pycite/)
[![Documentation Status](https://readthedocs.org/projects/pycite/badge/?version=latest)](https://pycite.readthedocs.io/en/latest/?badge=latest)
[![Total Downloads](https://pepy.tech/badge/pycite)](https://pepy.tech/project/pycite)
[![Monthly Downloads](https://pepy.tech/badge/pycite/month)](https://pepy.tech/project/pycite)
[![Weekly Downloads](https://pepy.tech/badge/pycite/week)](https://pepy.tech/project/pycite)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Nelson-Gon/pycite/graphs/commit-activity)
[![GitHub last commit](https://img.shields.io/github/last-commit/Nelson-Gon/pycite.svg)](https://github.com/Nelson-Gon/pycite/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Nelson-Gon/pycite.svg)](https://GitHub.com/Nelson-Gon/pycite/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/Nelson-Gon/pycite.svg)](https://GitHub.com/Nelson-Gon/pycite/issues?q=is%3Aissue+is%3Aclosed)



`pycite` is a simple to use `python` citations generator.


**Supported Reference Styles**

- [x] Harvard 

**Supported Paper Sources**

- [x] NCBI

- [x] Pubmed

- [x] ScienceDirect 

- [ ] JSTOR (**Support dropped on 5th November 2021** Why? Uses dynamic JS that we do not want to work with for now.)

**Supported file formats**

`pycite` generates citations given a file of the following types:

- [x] Text files (`.txt`)





# Installation

The simplest way to install the latest release is as follows:

```shell
pip install pycite

```

To install the development version:


Open the Terminal/CMD/Git bash/shell and enter

```shell

pip install git+https://github.com/Nelson-Gon/pycite.git

# or for the less stable dev version
pip install git+https://github.com/Nelson-Gon/pycite.git@dev

```

Otherwise:

```shell
# clone the repo
git clone git@github.com:Nelson-Gon/pycite.git
cd pycite
pip install .  

```

# Usage 

**Script Mode**

To use at the command line, please use:

```shell
python -m pycite -i testfiles/testlinks.txt -o testfiles/citations.txt
```

To get help:

```shell
python -m pycite --help
#usage: __main__.py [-h] -i INPUT_FILE -o OUTPUT_FILE
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -i INPUT_FILE, --input-file INPUT_FILE
#                        Path to an input file
#  -o OUTPUT_FILE, --output-file OUTPUT_FILE
#                        Path to an output file

```

**Programming Mode**

First, one needs to create an object of class `PyCite`

```shell
from pycite.pycite import PyCite
```

```shell
# Need an input-output file pair 
my_citations = PyCite(input_file="testfiles/testlinks.txt", output_file="testfiles/citations.txt")
```

To generate citations, one simply calls the `cite` method.

```shell
# This will write citations in the provided output file 
my_citations.cite()
```

The above creates citations as required (only the first line shown here). 
See [citations.txt](https://github.com/Nelson-Gon/pycite/blob/main/testfiles/citations.txt) for the full file.

```shell
Pohorille A, Wilson MA, & Shannon G (2017)  Flexible Proteins at the Origin of Life Life (Basel), 7(2),  23.  [Accessed 16/Sep/2021]
```

---

**Note**

`pycite` is free software that the author hopes could be of use to someone else and enable them to perform reproducible
science. 

If you have any concerns, especially regarding the papers used to test that the software works, 
please [contact](https://nelson-gon.github.io/social) the author. In the event that you notice that any of the papers used in the tests has been retracted, please immediately inform the author to remove that paper. 

Thank you very much and keep building, 

**For Science!**

To report any issues, suggestions or improvement, please do so 
at [issues](https://github.com/Nelson-Gon/pycite/issues). 

> “Before software can be reusable it first has to be usable.” – Ralph Johnson


