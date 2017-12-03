# ADAM : Question Answering System
A question answering system that extracts answers questions in natural language from Wikipedia. Currently the answers 
extracted by the system are of an average to above average accuracy. I have identified the issues and I am working on 
improving the accuracy. Please checkout the road-map of this project to know more about the status of this project.
You can also follow by blog [shirishkadam.com](https://www.shirishkadam.com/)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2e669faacb12496f9d4e97f3a0cfc361)](https://www.codacy.com/app/5hirish/adam_qas?utm_source=github.com&utm_medium=referral&utm_content=5hirish/adam_qas&utm_campaign=badger)

## Developed & Maintained by team Alleviate
Inspired by *IBM Watson* and *START*

### Features :
* Wikipedia as knowledge source
* Question Classification using Support Vector Classifier (Currently not used in Question Analysis flow)
* A 2 step Vector Space model used for Answer Extraction
* Merges top 5 answers to form final answer

### Documentation:
Find more in depth documentation about the system with its research paper and system architecture here: [ARCHI.md](/doc/ARCHI.md)

### Requirements :
###### Python3 - [Python v3.5](https://docs.python.org/3/)
* [spaCy v2.0.3](https://spacy.io/)
* [scikit-learn v0.19.1](http://scikit-learn.org/)
* [gensim v3.0.1](https://radimrehurek.com/gensim/)
* [pandas v0.21](http://pandas.pydata.org/)
* [wikipedia v1.10](https://pypi.python.org/pypi/wikipedia/)

To execute adam qas `python qa_init.py` at `adam/src`

##### Development Environment :
* OS - Linux Mint 18.3 (64 bit)
* IDE - Intellij IDEA 2017 / PyCharm 2017

### Road-Map :
- [ ] Replace Wikipedia APIs with in house scraper
- [ ] Anaphora resolution
- [ ] Replace the rule based query constructor
- [ ] Improve the VSM for answer extraction

### Branches :
1. master - Master Branch
2. dev - Development Branch

__Coding Standards__ : Follow these coding style for [Python](http://docs.python-guide.org/en/latest/writing/style/)

## Copyright License :
![alt text](https://licensebuttons.net/l/by-nc-nd/3.0/88x31.png "CC BY-NC-ND")

Attribution-NonCommercial-NoDerivs 

CC BY-NC-ND

Visit [Creative Commons](https://creativecommons.org/licenses/by-nc-nd/4.0/)

