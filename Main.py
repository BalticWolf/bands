#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from pyquery import PyQuery
from DbConnection import NeoDb
from Band import Band


def main():
    # make_url_file('./data/rym_extract')
    # with open('./data/urls', 'r') as f:
    #     f.readline()
    # neo = NeoDb("bolt://127.0.0.1:7687", "neo4j", "bands")
    # session = neo.get_session()
    # for band in Band.get_all(session):
    #     print(band["name"])

    band = get_info_from_url('./data/pages/The Smashing Pumpkins - Sonemic _ Rate Your Music music database.html')
    print(band)


def make_url_file(path):
    rym = pd.read_csv(path, encoding='utf-8')
    rym.columns = rym.columns.map(lambda x: x.strip(' '))
    rym = rym.iloc[:, 1:3]
    rym['First Name'] = rym['First Name'].apply(str)
    rym = rym.drop_duplicates()

    artists = rym.apply(lambda row: row[0] + ' ' + row[1], axis=1)
    artists = artists.map(lambda x: x.replace('nan ', ''))

    urls = artists.map(lambda x: make_url(x))
    urls.to_csv('./data/urls', header=False, index=False)


def make_url(band_name):
    base_url = "https://rateyourmusic.com/artist/"

    name = band_name\
        .replace(' O)))', '-o') \
        .replace(' ', '_') \
        .replace('/', '_') \
        .replace(',', '_') \
        .replace('&amp;', 'and') \
        .lower()\
        .replace("'", "")\
        .replace('à', 'a')\
        .replace('â', 'a')\
        .replace('ä', 'a')\
        .replace('è', 'e')\
        .replace('é', 'e')\
        .replace('ê', 'e')\
        .replace('ë', 'e')\
        .replace('î', 'i')\
        .replace('ï', 'i')\
        .replace('ô', 'o')\
        .replace('ö', 'o')\
        .replace('ó', 'o')\
        .replace('û', 'u')\
        .replace('ü', 'u')

    return base_url + name


def get_info_from_url(link):
    page = PyQuery(filename=link)

    # extract band name
    name = page('div.artist_page_name h1').text()

    # extract band information
    info = page('div.artist_page_info')

    # extract list of headers within band information section
    headers = [header.text for header in info('div.artist_page_info_hdr')]

    # information is structured in 2 different ways
    data1 = [item.text for item in info('div.artist_page_info_data')]
    data2 = [item.text() for item in info('div.artist_page_info_data').items('p')]

    # gather information: replace trailing None values of elts1 by elts2
    items = data1[:-len(data2)] + data2

    # create key-value pairs
    band = dict(list(zip(headers, items)))
    band['Name'] = name

    return band


if __name__ == '__main__':
    main()
