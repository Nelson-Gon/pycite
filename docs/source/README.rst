
pycite: Python Citations Generator
==================================


.. image:: https://badge.fury.io/py/pycite.svg
   :target: https://pypi.python.org/pypi/pycite/
   :alt: PyPI version fury.io


.. image:: http://www.repostatus.org/badges/latest/active.svg
   :target: http://www.repostatus.org/#active
   :alt: Project Status
 

.. image:: https://codecov.io/gh/Nelson-Gon/pycite/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Nelson-Gon/pycite?branch=master
   :alt: Codecov


.. image:: https://github.com/Nelson-Gon/pycite/workflows/Test-Package/badge.svg
   :target: https://github.com/Nelson-Gon/pycite/workflows/Test-Package/badge.svg
   :alt: Test-Package


.. image:: https://travis-ci.com/Nelson-Gon/pycite.svg?branch=master
   :target: https://travis-ci.com/Nelson-Gon/pycite.svg?branch=master
   :alt: Travis Build


.. image:: https://img.shields.io/pypi/l/pycite.svg
   :target: https://pypi.python.org/pypi/pycite/
   :alt: PyPI license


.. image:: https://readthedocs.org/projects/pycite/badge/?version=latest
   :target: https://pycite.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://pepy.tech/badge/pycite
   :target: https://pepy.tech/project/pycite
   :alt: Total Downloads


.. image:: https://pepy.tech/badge/pycite/month
   :target: https://pepy.tech/project/pycite
   :alt: Monthly Downloads


.. image:: https://pepy.tech/badge/pycite/week
   :target: https://pepy.tech/project/pycite
   :alt: Weekly Downloads


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Nelson-Gon/pycite/graphs/commit-activity
   :alt: Maintenance


.. image:: https://img.shields.io/github/last-commit/Nelson-Gon/pycite.svg
   :target: https://github.com/Nelson-Gon/pycite/commits/master
   :alt: GitHub last commit


.. image:: https://img.shields.io/github/issues/Nelson-Gon/pycite.svg
   :target: https://GitHub.com/Nelson-Gon/pycite/issues/
   :alt: GitHub issues


.. image:: https://img.shields.io/github/issues-closed/Nelson-Gon/pycite.svg
   :target: https://GitHub.com/Nelson-Gon/pycite/issues?q=is%3Aissue+is%3Aclosed
   :alt: GitHub issues-closed


``pycite`` is a simple to use ``python`` citations generator.

**Supported Reference Styles**


* [ ] Harvard 

**Supported file formats**

``pycite`` generates citations given a file of the following types:


* [ ] Text files (\ ``.txt``\ )

Installation
============

The simplest way to install the latest release is as follows:

.. code-block:: shell

   pip install pycite

To install the development version:

Open the Terminal/CMD/Git bash/shell and enter

.. code-block:: shell


   pip install git+https://github.com/Nelson-Gon/pycite.git

   # or for the less stable dev version
   pip install git+https://github.com/Nelson-Gon/pycite.git@dev

Otherwise:

.. code-block:: shell

   # clone the repo
   git clone git@github.com:Nelson-Gon/pycite.git
   cd pycite
   python3 setup.py install

Usage
=====

First, one needs to create an object of class ``PyCite``

.. code-block:: python

   from pycite.pycite import PyCite

.. code-block:: python

   my_citations = PyCite("path_to_links_file")

To generate citations, one simply calls the ``cite`` method.

.. code-block:: python

   mycitations.cite()

----

**Thank you very much and Keep Building**. 

..

   To report any issues, suggestions or improvement, please do so 
   at `issues <https://github.com/Nelson-Gon/pycite/issues>`_. 

   “Before software can be reusable it first has to be usable.” – Ralph Johnson

