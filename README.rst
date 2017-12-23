ADAM -- Question Answering System
=================================

A question answering system that extracts answers questions in natural
language from Wikipedia. Inspired by *IBM Watson* and *START*. Currently
the answers extracted by the system are of an average to above average
accuracy. I have identified the issues and I am working on improving the
accuracy. Please checkout the road-map of this project to know more
about the status of this project. You can also follow by blog
`shirishkadam.com <https://www.shirishkadam.com/>`__

|Codacy Badge| |Twitter|

Developed & Maintained by team Alleviate
----------------------------------------

Features
~~~~~~~~

-  Extract information from Wikipedia
-  Classify questions with regular expression (default)
-  Classify questions with a SVM (optional)
-  Vector space model used for answer extraction
-  Rank candidate answers
-  Merge top 5 answers into one response

TODO
~~~~

-  [ ] Replace Wikipedia APIs with custom scraper
-  [ ] Anaphora resolution in both questions and answers
-  [ ] Machine learning query constructor rather than rule-based
-  [ ] Improve vector space language model for answer extraction

Documentation:
~~~~~~~~~~~~~~

Find more in depth documentation about the system with its research
paper and system architecture here: `ARCHI.md </doc/ARCHI.md>`__

Requirements
~~~~~~~~~~~~

Requirements listed in ``requirements.txt``

Requirements.txt
----------------

`Python 3 <https://docs.python.org/3/>`__

-  `spaCy>=2.0.3 <https://spacy.io/>`__
-  `scikit-learn>=0.19.1 <http://scikit-learn.org/>`__
-  `gensim>=3.0.1 <https://radimrehurek.com/gensim/>`__
-  `pandas>=0.21 <http://pandas.pydata.org/>`__
-  `wikipedia>=1.4.0 <https://pypi.python.org/pypi/wikipedia/>`__
-  `pyenchant>=2.0.0 <https://pypi.python.org/pypi/pyenchant/>`__
-  `autocorrect>=0.3.0 <https://pypi.python.org/pypi/autocorrect/>`__

Getting Started
---------------

.. code:: bash

    $ git clone https://github.com/totalgood/adam_qas.git
    $ cd adam_qas
    $ pip install -r requirements.txt
    $ python -m spacy download en_core_web_md
    $ pip install -e .
    $ python qas/qa_init.py

Branches :
~~~~~~~~~~

1. master - Master Branch
2. dev - Development Branch

**Coding Standards** : Follow these coding style for
`Python <http://docs.python-guide.org/en/latest/writing/style/>`__

qas
===

Add a short description here!

Description
-----------

A longer description of your project goes here...

Note
----

This project has been set up using PyScaffold 2.5.8. For details and
usage information on PyScaffold see http://pyscaffold.readthedocs.org/.

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/2e669faacb12496f9d4e97f3a0cfc361
   :target: https://www.codacy.com/app/5hirish/adam_qas?utm_source=github.com&utm_medium=referral&utm_content=5hirish/adam_qas&utm_campaign=badger
.. |Twitter| image:: https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow
   :target: https://twitter.com/intent/follow?screen_name=5hirish
