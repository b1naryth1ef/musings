from peewee import *

db = SqliteDatabase("data.db")

class Entry(Model):
    class Meta:
        database = db

    cid = CharField()
    sub = CharField(index=True)
    val = IntegerField(index=True)

if __name__ == "__main__":
    Entry.drop_table(True)
    Entry.create_table(True)