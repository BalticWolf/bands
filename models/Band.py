#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Band(object):
    def __init__(self, data):
        self.name = ''
        if 'Name' in data:
            self.name = data['Name']

        self.formed = ''
        if 'Formed' in data:
            self.formed = data['Formed']

        self.disbanded = ''
        if 'Disbanded' in data:
            self.disbanded = data['Disbanded']

    @staticmethod
    def get_all(session):
        with session:
            results = session.run("MATCH (a:Band) "
                                  "RETURN a.name AS name "
                                  "ORDER BY name")
        return results

    def insert(self, session):
        with session:
            session.run("MERGE (a:Band {"
                        "name: {name},"
                        "formed: {formed},"
                        "disbanded: {disbanded}})",
                        {"name": self.name,
                         "formed": self.formed,
                         "disbanded": self.disbanded})

        return "inserted band"
