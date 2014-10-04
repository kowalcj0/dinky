D - I - N - K - Y
-------------------------------------------------------------------------------

It's a example project that uses:
* [requests](http://docs.python-requests.org/en/latest/) to fetch the webpage
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) to extract page contents
* [python-epub-builder](https://code.google.com/p/python-epub-builder/) to create an ePub file
  * which relies on other tools:
  * [Genshi](http://genshi.edgewall.org/) HTML, XML parsing, generating, and processing library
  * [lxml](http://lxml.de/) is a XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt
  * [IPDF/epubcheck](https://github.com/IDPF/epubcheck) to validate created ePub file


What it does:
------------
1. fetch the webpage
2. Extract page (main) content
3. Create an ePub file
4. validate the created ePub file


Installation:

    pip install -r requirements --upgrage

Run:

    ./test_soup.py

Then check the `output` dir
