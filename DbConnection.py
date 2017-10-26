#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from neo4j.v1 import GraphDatabase, basic_auth


class NeoDb(object):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def get_session(self):
        return self.driver.session()

# session.run("CREATE (a:Person {name: {name}, title: {title}})",
#             {"name": "Arthur", "title": "King"})
#
# result = session.run("MATCH (a:Person) WHERE a.name = {name} "
#                      "RETURN a.name AS name, a.title AS title",
#                      {"name": "Arthur"})
# for record in result:
#     print("%s %s" % (record["title"], record["name"]))
#
# session.close()
