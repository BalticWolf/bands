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
        if key in band and band[key] is not None:
            band[key] = re.compile('\d{4}').search(band[key]).group()
        else:
            band[key] = ''

    # format data
    band['Members'] = to_dict_list(band['Members'])

    return band


def to_dict_list(raw_members):
    """
    :param raw_members: string containing all band members and their features
    :return: [{}] representing all members and their features
    """
    # split band members seperated by commas, (except commas between brackets)
    members = re.split(",(?![^([]*?(\)|\]))", raw_members)

    # transform members into list of dict
    members = [member_to_dict(member) for member in members]

    return members


def member_to_dict(raw_member):
    """
    :param raw_member: string representing a band member
    :return: {'Name': ... [, 'Instruments': ... [, 'Aka': ... [, 'Periods': ... ]]]} representing a band member
    """
    def get_aka(str_member):
        """aka is found between square brackets"""
        return re.search('(?<=\[).*?(?=\])', str_member)

    def get_features(str_member):
        """features, ie instruments and periods of activity, are found between parenthesis"""
        raw_features = ''
        opt_feat = re.search('(?<=\().*?(?=\))', str_member)

        if opt_feat:
            raw_features = opt_feat.group()

        features = re.split(', (?=\d)', raw_features, 1)
        instruments = features[0].strip()
        periods = ''

        if len(features) > 1:
            periods = features[1]

        return instruments, periods

    def get_name(str_member):
        name = re.sub('\[.*?\]', '', str_member)
        name = re.sub('\(.*?\)', '', name)

        return name.strip()

    def get_periods(str_member):
        return transform_periods(str_member)

    if raw_member is None or len(raw_member) == 0:
        member = None
    else:
        member = {'Name': get_name(raw_member)}

        aka_pattern = get_aka(raw_member)
        instr, per = get_features(raw_member)

        if aka_pattern and len(aka_pattern.group()) > 0:
            member['Aka'] = aka_pattern.group()

        if instr:
            member['Instruments'] = instr

        if per:
            member['Periods'] = transform_periods(per)

    return member


def transform_periods(raw_periods):
    """
    :param raw_periods: string representing all the activity periods of a band member
    :return: [{'Start': ... , 'End': ... }, ... ] representing all the activity periods
    """
    periods = raw_periods.split(',')
    for i in range(len(periods)):
        periods[i] = transform_period(periods[i])
    periods = [x for x in periods if x is not None]
    # return none if periods is the empty list
    return periods


def transform_period(raw_period):
    """
    :param raw_period: string representing a period of activity of a band member
    :return: {'Start': ... , 'End': ... } representing the activity period
    """
    def format_year(str_year):
        """
        :param str_year: string representing a year
        :return: either an integer representing a year on 4 digits, or an empty string
        """
        try:
            int_year = int(str_year.strip(', '))
            if int_year < 100:
                # 0 <= year <= 99
                if int_year + 2000 <= date.today().year:
                    # 2000 <= year + 2000 <= current year
                    int_year += 2000
                else:
                    # year + 2000 > current year (
                    int_year += 1900

            return int_year

        except ValueError:
            return ''

    if len(raw_period) == 0:
        period = None
    else:
        limits = raw_period.split('-')

        # By default, the member started and stopped activity the same year
        start_year = format_year(limits[0])
        period = {'Start': start_year, 'End': start_year}

        # Adjust when end date is specified
        if len(limits) > 1:
            period['End'] = format_year(limits[1])

    return period
