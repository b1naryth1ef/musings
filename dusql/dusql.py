#!/usr/bin/env python
from peewee import *
import humanfriendly, fileinput, argparse
import sys, os

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--table", help="DB Table Name", default="fstest", required=True)
parser.add_argument("-f", "--file", help="Load data from a du file dump", default=None)
parser.add_argument("-c", "--clear", help="Recreate the db table before inserting anything", action='store_true')

db = Proxy()

class File(Model):
    class Meta:
        database = db

    path = TextField()
    size = BigIntegerField()

    @classmethod
    def from_du(cls, line):
        self = cls()
        if '\t' not in line:
            return
        a, b = line.split("\t", 1)
        self.size = humanfriendly.parse_size(a.strip())
        self.path = b.strip()
        return self

def db_from_path(path):
    _db = PostgresqlDatabase(path, user="b1n", password="b1n")
    db.initialize(_db)

if __name__ == "__main__":
    args = vars(parser.parse_args())

    db_from_path(args["table"])

    # Recreate table
    if args["clear"]:
        File.drop_table()
        File.create_table()

    if args["file"]:
        f = open(args["file"], "r")
    else:
        f = sys.stdin

    for line in f:
        i = File.from_du(line)
        if i: i.save()

