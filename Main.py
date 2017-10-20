#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd


def main():
    rym = pd.read_csv('./data/rym_extract', encoding='utf-8')
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


if __name__ == '__main__':
    main()
