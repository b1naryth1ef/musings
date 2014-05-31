from peewee import *

db = SqliteDatabase("data.db")

class Entry(Model):
    class Meta:
        database = db

    cid = CharField()
    sub = CharField(index=True)
    val = FloatField(index=True)
    body = TextField()
    ups = IntegerField()
    downs = IntegerField()
    link_url = CharField()
    link_title = CharField()
    author = CharField()

if __name__ == "__main__":
    Entry.drop_table(True)
    Entry.create_table(True)