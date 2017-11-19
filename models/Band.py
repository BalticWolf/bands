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

        self.members = []
        if 'Members' in data:
            self.members = data['Members']

    @staticmethod
    def get_all(session):
        with session:
            results = session.run("MATCH (b:Band) "
                                  "RETURN b.name AS name "
                                  "ORDER BY name")
        return results

    def insert(self, session):
        with session:
            session.run("MERGE (b:Band {name: {name}}) "
                        "ON MATCH SET b.formed = {formed}, b.disbanded = {disbanded}",
                        {"name": self.name,
                         "formed": self.formed,
                         "disbanded": self.disbanded})

            for member in self.members:
                session.run("MERGE (m:Member {"
                            "name: {member_name}})",
                            {"member_name": member['Name']})

                session.run("MATCH (b: Band {name: {band_name}}), (m:Member {name: {member_name}}) "
                            "MERGE (m)-[r:PLAYED_IN {instruments: {instruments}}]->(b)",
                            {"member_name": member['Name'],
                             "instruments": member['Instruments'],
                             "band_name": self.name})

                # if 'Periods' in member:
                #     session.run("MATCH (m:Member {name: {member_name}})-[r:PLAYED_IN]->(b: Band {name: {band_name}})"
                #                 "SET r.periods = {periods}",
                #                 {"member_name": member['Name'],
                #                  "periods": member['Periods'],
                #                  "band_name": self.name})

        return "inserted band"

    def __repr__(self):
        return 'name: ' + self.name + ', formed: ' + self.formed + ', disbanded: ' + self.disbanded + ', members: ' + \
               str(self.members)
