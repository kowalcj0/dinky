D - I - N - K - Y
-------------------------------------------------------------------------------

It's a example project that uses:
* [requests](http://docs.python-requests.org/en/latest/) to fetch the webpage
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) to extract page contents
* [python-readability](https://github.com/buriy/python-readability) pulls out the main body text and cleans it up
* [python-epub-builder](https://code.google.com/p/python-epub-builder/) to create an ePub file
  * which relies on other tools:
  * [Genshi](http://genshi.edgewall.org/) HTML, XML parsing, generating, and processing library
  * [lxml](http://lxml.de/) is a XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt
  * [IPDF/epubcheck](https://github.com/IDPF/epubcheck) to validate created ePub file


What it does:
===============
1. fetch the webpage
2. Extract page (main) content
3. Create an ePub file
4. validate the created ePub file


Installation:
===============

    pip install -r requirements --upgrage


Run:
===============

    ./test_soup.py
    ./test_readability.py

Then check the `output` dir


Running locally
===============
To run the service locally:

    python setup.py develop
    python dinky/

Running tests and generating code coverage
==========================================
To have a "clean" target from build artifacts:

    make clean

To run all unit tests and generate a HTML code coverage report along with a
JUnit XML report in tests/unit/reports:

    make test

To run pyLint and generate a HTML report in tests/unit/reports:

    make pylint

To run all behave tests and generate a JUnit XML report in tests/behave/reports:

    make behave
