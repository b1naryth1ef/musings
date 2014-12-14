from peewee import *
import time

db = PostgresqlDatabase('fstest', user="b1n", password="b1n")

class Test(Model):
    class Meta:
        database = db
    a = TextField()
    b = CharField()
    c = IntegerField()
    d = BigIntegerField()

Test.drop_table(True)
Test.create_table(True)

start = time.time()
count = 0
while True:
    if (time.time() - start) >= 60:
        print "Count: %s" % count
        print "%s/second" % (count / 60.0)
        break
    Test(a="test", b="test", c=1, d=1.1).save()
    count += 1


