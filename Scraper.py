#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import date
from pyquery import PyQuery


def get_info_from_url(link):
    """
    :param link: file or link to handle
    :return: {} representing a band
    """
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

    # merge information: replace trailing None values of data1 by data2
    items = data1[:-len(data2)] + data2

    # create key-value pairs
    band = dict(list(zip(headers, items)))
    band['Name'] = name

    # clean data
    for key in ['Formed', 'Disbanded']:
        if key in band:
            band[key] = band[key].strip(' ').strip(',')

    # format data
    band['Members'] = to_dict_list(band['Members'])

    return band


def to_dict_list(raw_members):
    """
    :param raw_members: string containing all band members and their features
    :return: [{}] representing all members and their features
    """
    keys = ['Name', 'Instruments', 'Periods']

    # get a list of band members, ignoring the last parenthesis of raw_members
    members = raw_members[:-1].split('), ')

    # separate member name from other features
    members = [member.replace(' (', '|') for member in members]

    # separate instruments from active periods
    members = [re.sub(', (?=\d)', '|', member, 1) for member in members]

    # split member features
    members = [member.split('|') for member in members]

    for member in members:
        # put instruments and active periods in lists
        for i in list(range(1, len(member))):
            member[i] = member[i].split(', ')

            # transform periods in list of dict [{'start':, 'end':}]
            if i == 2:
                member[i] = transform_periods(member[i])

    # transform members as list of dict
    members = [dict(zip(keys, member)) for member in members]

    return members


def transform_periods(raw_periods):
    """
    :param raw_periods: string representing all the activity periods of a band member
    :return: [{'Start': ... , 'End': ... }, ... ] representing all the activity periods
    """
    periods = raw_periods
    for i in range(len(periods)):
        periods[i] = transform_period(periods[i])

    return periods


def transform_period(raw_period):
    """
    :param raw_period: string representing a period of activity of a band member
    :return: {'Start': ... , 'End': ... } or {'Start': ... } representing the activity period
    """
    period = {}
    limits = raw_period.split('-')

    def format_year(str_year):
        """
        :param str_year: string representing a year, on 2 or 4 digits
        :return: an integer representing a year on 4 digits
        """
        int_year = int(str_year)

        if int_year < 100:
            # 0 <= year <= 99
            if int_year + 2000 <= date.today().year:
                # 2000 <= year + 2000 <= current year
                int_year += 2000
            else:
                # year + 2000 > current year (
                int_year += 1900

        return int_year

    # No end date: the member started and stopped activity the same year
    if len(limits) == 1:
        # the string is not empty
        if len(limits[0]) > 0:
            period = {'Start': int(limits[0]), 'End': int(limits[0])}

    # End date section specified
    elif len(limits) == 2:
        year = limits[1]

        if year in ['present', 'pres', 'pres.', 'current', '?']:
            # the member is still currently active
            period = {'Start': int(limits[0]), 'End': ''}

        else:
            # the member is no longer active
            period = {'Start': int(limits[0]), 'End': format_year(year)}

    return period
