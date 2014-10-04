#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import ez_epub
import langid
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content.decode("utf-8").encode("utf-8"))


def get_lang(soup):
    lang = ""
    if soup.html.has_attr("lang"):
        soup_lang = soup.html.get("lang")
    det_lang, det_conf = langid.classify(get_just_text(soup))
    if det_conf > 0.8:
        lang = det_lang
    else:
        lang = soup_lang
    return lang


def get_title(soup):
    title = soup.find_all("title", limit=1)[0].text
    if not title: 
        title = "Generic Title"
    return title


def get_just_text(soup):
    text = ""
    for paragraph in soup.find_all("p"):
        text += paragraph.text
    return text


def get_sections(soup):
    sections = []
    for paragraph in soup.find_all("p"):
        section = ez_epub.Section()
        section.title = paragraph.text[:20]
        section.text.append(paragraph.text)
        sections.append(section)
    return sections


def main():
    url = "http://pl.wikipedia.org/wiki/Rewolucja_pa%C5%BAdziernikowa"
    soup = get_soup(url)

    book = ez_epub.Book()
    book.impl.addCover(r'templates/cover.jpg')
    book.lang = get_lang(soup)
    book.title = get_title(soup)
    book.authors = ['Wikipedia']
    book.sections = get_sections(soup)
    book.impl.addCreator('kowalcj0')
    book.impl.addMeta('date', '2014', event = 'conversion')

    book.make(r'output/article')


if __name__ == '__main__':
    main()

