#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

from DbConnection import NeoDb
from models.Band import Band
from Scraper import get_info_from_url


def main():
    # neodb instance
    neo = NeoDb("bolt://127.0.0.1:7687", "neo4j", "bands")
    session = neo.get_session()

    for dirname, dirnames, filenames in os.walk('./data/pages'):
        # browse folder
        for filename in filenames:
            # exclude files causing errors
            if filename not in [
                '.DS_Store',
                'House of Broken Promises - Sonemic _ Rate Your Music music database.html',
                'Puscifer - Sonemic _ Rate Your Music music database.html',
                'Rob Zombie - Sonemic _ Rate Your Music music database.html'
            ]:
                path = os.path.join(dirname, filename)
                band_data = get_info_from_url(path)

                band = Band(band_data)
                print(band)
                band.insert(session)
    session.close()


if __name__ == '__main__':
    main()
