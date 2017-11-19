#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Member(object):
    def __init__(self, name):
        self.name = name

    def insert(self, session):
        session.run("MERGE (m:Member {"
                    "name: {member_name}})",
                    {"member_name": self.name})

    def __repr__(self):
        return self.name
