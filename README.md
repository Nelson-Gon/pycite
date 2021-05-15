# pycite: Python Citations Generator 


[![DOI](https://zenodo.org/badge/367264942.svg)](https://zenodo.org/badge/latestdoi/367264942)
[![PyPI version fury.io](https://badge.fury.io/py/pycite.svg)](https://pypi.python.org/pypi/pycite/)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active) 
[![Codecov](https://codecov.io/gh/Nelson-Gon/pycite/branch/main/graph/badge.svg)](https://codecov.io/gh/Nelson-Gon/pycite?branch=main)
![Test-Package](https://github.com/Nelson-Gon/pycite/workflows/Test-Package/badge.svg)
[![Build Status](https://www.travis-ci.com/Nelson-Gon/pycite.svg?branch=main)](https://www.travis-ci.com/Nelson-Gon/pycite)
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

**Supported file formats**

`pycite` generates citations given a file of the following types:

- [ ] Text files (`.txt`)





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
python3 setup.py install

```

# Usage 

First, one needs to create an object of class `PyCite`

```python
from pycite.pycite import PyCite
```

```python
my_citations = PyCite("testfiles/testlinks.txt")
```

To generate citations, one simply calls the `cite` method.

```python
my_citations.cite()
```



---

**Thank you very much and Keep Building**. 

> To report any issues, suggestions or improvement, please do so 
at [issues](https://github.com/Nelson-Gon/pycite/issues). 

> “Before software can be reusable it first has to be usable.” – Ralph Johnson


