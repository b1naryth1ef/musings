from database import Entry
from collections import *
from peewee import *

def get(value):
    return lambda i: getattr(i, value)
    
def get_unique_subs():
    return map(get("sub"), Entry.select().distinct(Entry.sub))

def get_all_sub_polaritys():
    return map(get_sub_polarity, get_unique_subs())

def get_sub_polarity(sub):
    q = list(Entry.select(fn.Avg(Entry.val).alias('avg')).where(Entry.sub == sub))
    return q[0].avg


if __name__ == '__main__':
    #print "Unique Subs w/ count:\n %s" % Counter(get_unique_subs())
    for sub in get_unique_subs():
        print "%s Polarity: %s" % (sub, get_sub_polarity(sub))
