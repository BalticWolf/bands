#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Band(object):
    def __init__(self):
        self.name = ''

    @staticmethod
    def get_all(session):
        with session:
            results = session.run("MATCH (a:Band) "
                                  "RETURN a.name AS name "
                                  "ORDER BY name")
        return results


    @staticmethod
    def insert(session, data):
        return 'inserted band'