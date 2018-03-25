# CONTIRUBING

Adam QAS is a community-maintained project and we happily accept contributions.

If you wish to add a new feature or fix a bug:

1. Check for [open issues](https://github.com/5hirish/adam_qas/issues) or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the [Adam QAS](https://github.com/5hirish/adam_qas) repository on Github to start making your changes.
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to [AUTHORS.rst](/AUTHORS.rst).

```bash 
$ git checkout dev -b feature/my-new-feature 
$ git pull origin master
```
_Note:_ Follow [PEP8](http://docs.python-guide.org/en/latest/writing/style/) codding style.

## Running the tests

We use some external dependencies, multiple interpreters and code coverage analysis while running test suite. Our Makefile handles much of this for you as long as you’re running it inside of a virtualenv:
```bash
$ pytest tests
```
Our test suite runs continuously on Travis CI with every pull request to `master`.

## HELP REQUIRED

To find where you can help, search for the following tags:
* `#TODO:` The tasks which are pending or yet not taken up
* `#FIXME:` The tasks which require some attending to do
* `#HELP:` The tasks which are require some help

You can also help in making the Wikipedia parser more robust by adding more XPath filters that remove irrelevant information or extract and format relevant information.