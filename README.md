# ADAM -- Question Answering System

A question answering system that extracts answers questions in natural language from Wikipedia. Inspired by *IBM Watson* and *START*. Currently the answers 
extracted by the system are of an average to above average accuracy. I have identified the issues and I am working on 
improving the accuracy. Please checkout the road-map of this project to know more about the status of this project.
You can also follow by blog [shirishkadam.com](https://www.shirishkadam.com/)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2e669faacb12496f9d4e97f3a0cfc361)](https://www.codacy.com/app/5hirish/adam_qas?utm_source=github.com&utm_medium=referral&utm_content=5hirish/adam_qas&utm_campaign=badger)
[![Twitter](https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=5hirish)

## Developed & Maintained by team Alleviate

### Features

* Extract information from Wikipedia
* Classify questions with regular expression (default)
* Classify questions with a SVM (optional)
* Vector space model used for answer extraction
* Rank candidate answers
* Merge top 5 answers into one response

### TODO

- [ ] Replace Wikipedia APIs with custom scraper
- [ ] Anaphora resolution in both questions and answers
- [ ] Machine learning query constructor rather than rule-based
- [ ] Improve vector space language model for answer extraction

### Documentation:

Find more in depth documentation about the system with its research paper and system architecture here: [ARCHI.md](/doc/ARCHI.md)

### Requirements

Requirements listed in `requirements.txt`

## Requirements.txt

[Python 3](https://docs.python.org/3/)

* [spaCy>=2.0.3](https://spacy.io/)
* [scikit-learn>=0.19.1](http://scikit-learn.org/)
* [gensim>=3.0.1](https://radimrehurek.com/gensim/)
* [pandas>=0.21](http://pandas.pydata.org/)
* [wikipedia>=1.4.0](https://pypi.python.org/pypi/wikipedia/)
* [pyenchant>=2.0.0](https://pypi.python.org/pypi/pyenchant/)
* [autocorrect>=0.3.0](https://pypi.python.org/pypi/autocorrect/)

## Getting Started

```bash
$ git clone https://github.com/totalgood/adam_qas.git
$ cd adam_qas
$ pip install -r requirements.txt
$ python -m spacy download en_core_web_md
$ pip install -e .
$ python qas/qa_init.py
```


### Branches :
1. master - Master Branch
2. dev - Development Branch

__Coding Standards__ : Follow these coding style for [Python](http://docs.python-guide.org/en/latest/writing/style/)

qas
===

Add a short description here!

Description
-----------

A longer description of your project goes here...

Note
----

This project has been set up using PyScaffold 2.5.8. For details and
usage information on PyScaffold see
<http://pyscaffold.readthedocs.org/>.
