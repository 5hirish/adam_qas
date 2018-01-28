# ADAM -- Question Answering System

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2e669faacb12496f9d4e97f3a0cfc361)](https://www.codacy.com/app/5hirish/adam_qas?utm_source=github.com&utm_medium=referral&utm_content=5hirish/adam_qas&utm_campaign=badger)
[![Codecov](https://codecov.io/gh/5hirish/adam_qas/branch/master/graph/badge.svg)](https://codecov.io/gh/5hirish/adam_qas)
[![Build Status](https://travis-ci.org/5hirish/adam_qas.svg?branch=master)](https://travis-ci.org/5hirish/adam_qas)
[![Slack](https://img.shields.io/badge/slack-adam__qas-red.svg)](https://join.slack.com/t/alleviatenlp/shared_invite/enQtMjk4NzEwNjI0MTc4LTA0MmQ3NWIyNjIwYjYwNDVlZGU3NzkwN2RiZWJjNDlhY2Y1YmQ5ZGUxMjRkYjE5NTVlZWZhYjY5MWNhY2QzNjM)
[![Twitter](https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=5hirish)

A question answering system that extracts answers questions in natural language from Wikipedia.
Inspired by *IBM Watson* and *START*.
Currently the answers extracted by the system are moderately accurate.
Follow the creator's blog at [shirishkadam.com](https://www.shirishkadam.com/) for updates on progress.

## Getting Started

Elasticsearch is being used to store and index the scrapped and parsed texts from Wikipedia.
`Elasticsearch 6.X` installation guide can be found at [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html). 
You might have to start the elasticsearch search service.

```bash
$ git clone https://github.com/5hirish/adam_qas.git
$ cd adam_qas
$ pip install -r requirements.txt
$ python qas/adam.py "When was linux kernel version 4.0 released ?"
```

_Note:_ The above installation downloads the best-matching default english language model for spaCy. But to improve the model's accuracy you can install other models too. Read more at [spaCy docs](https://spacy.io/usage/models).

```bash
$ python -m spacy download en_core_web_md
```
## References

Find more in depth documentation about the system with its research paper and system architecture [here](docs/ARCHI.md)

## Requirements

* [Python 3.X](https://docs.python.org/3/)
* [Elasticsearch 6.X](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)

Python Package dependencies listed in [requirements.txt](requirements.txt)

### Features

* Extract information from Wikipedia
* Classify questions with regular expression (default)
* Classify questions with a SVM (optional)
* Vector space model used for answer extraction
* Rank candidate answers
* Merge top 5 answers into one response

### TODO

- [x] Replace Wikipedia APIs with custom scraper
- [x] Storing extracted data in database (elasticsearch)
- [ ] Anaphora resolution in both questions and answers
- [ ] Machine learning query constructor rather than rule-based
- [ ] Improve vector space language model for answer extraction

### Contributions
Please see our [contributing documentation](docs/CONTRIBUTING.md) for some tips on getting started.

### Maintainers
* [@5hirish](https://github.com/5hirish) - Shirish Kadam
