#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import ez_epub
import langid
from readability.readability import Document
from bs4 import BeautifulSoup


def get_html(url):
    return requests.get(url).content.decode("utf-8").encode("utf-8")


def get_readability(html):
    html = Document(html).summary()
    return html


def get_soup_readability(html):
    from test_soup import get_just_text
    summary = Document(html).summary()
    soup = BeautifulSoup(summary)
    text = get_just_text(soup)
    return text


def get_lang(html):
    det_lang, det_conf = langid.classify(html)
    return det_lang


def get_title(html):
    title = Document(html).short_title()
    if not title: 
        title = "Generic Title"
    return title


def get_sections(html):
    sections = []
    section = ez_epub.Section()
    section.title = get_title(html)
    section.text.append(get_soup_readability(html))
    sections.append(section)
    return sections


def main():
    url = "http://pl.wikipedia.org/wiki/Rewolucja_pa%C5%BAdziernikowa"
    html = get_html(url)
   
    book = ez_epub.Book()
    book.impl.addCover(r'templates/cover.jpg')
    book.lang = get_lang(html)
    book.title = get_title(html)
    book.authors = ['Wikipedia']
    book.sections = get_sections(html)
    book.impl.addCreator('kowalcj0')
    book.impl.addMeta('date', '2014', event = 'conversion')

    book.make(r'output/readability')


if __name__ == '__main__':
    main()

