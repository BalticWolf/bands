#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase, basic_auth


class Band:
    def __init__(self):
        self.name = ''

    @staticmethod
    def get_all():
        driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "bands"))
        session = driver.session()
        results = session.run("MATCH (a:Band) "
                              "RETURN a.name AS name "
                              "ORDER BY name")

        session.close()

        return results
