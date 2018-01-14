# ADAM -- Question Answering System

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2e669faacb12496f9d4e97f3a0cfc361)](https://www.codacy.com/app/5hirish/adam_qas?utm_source=github.com&utm_medium=referral&utm_content=5hirish/adam_qas&utm_campaign=badger)
[![Build Status](https://travis-ci.org/5hirish/adam_qas.svg?branch=master)](https://travis-ci.org/5hirish/adam_qas)
[![Twitter](https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=5hirish)

A question answering system that extracts answers questions in natural language from Wikipedia.
Inspired by *IBM Watson* and *START*.
Currently the answers extracted by the system are moderately accurate.
Follow the creator's blog at [shirishkadam.com](https://www.shirishkadam.com/) for updates on progress.

## Getting Started

```bash
$ git clone https://github.com/5hirish/adam_qas.git
$ cd adam_qas
$ pip install -r requirements.txt
$ python -m spacy download en_core_web_md
$ python qas/adam.py "When was linux kernel version 4.0 released ?"
```

## References

Find more in depth documentation about the system with its research paper and system architecture [here](docs/ARCHI.md)

## Requirements

[Python 3](https://docs.python.org/3/)

Package dependencies listed in `requirements.txt`

* [spaCy>=2.0.3](https://spacy.io/)
* [scikit-learn>=0.19.1](http://scikit-learn.org/)
* [gensim>=3.0.1](https://radimrehurek.com/gensim/)
* [pandas>=0.21](http://pandas.pydata.org/)
* [wikipedia>=1.4.0](https://pypi.python.org/pypi/wikipedia/)

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
- [ ] Storing extracted data in database
- [ ] Anaphora resolution in both questions and answers
- [ ] Machine learning query constructor rather than rule-based
- [ ] Improve vector space language model for answer extraction

