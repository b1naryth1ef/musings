from database import Entry
from collections import *
from peewee import *

# Helpers
def get(value):
    return lambda i: getattr(i, value)

def gett(*values):
    return lambda i: [getattr(i, value) for value in values]
    
# Statistical functions
def get_unique_subs():
    """
    Returns a list of unique sub names that we have
    """
    return map(get("sub"), Entry.select(Entry.sub).distinct(Entry.sub))

def get_unique_sub_counts():
    """
    Returns a dictionary of subs to the number of entries we have for the
    sub
    """
    return dict(map(gett("sub", "count"), 
        Entry.select(Entry, fn.Count(Entry.sub).alias("count")).group_by(Entry.sub)))

def get_sub_polarity(sub):
    """
    Returns the polarity (based on sentiment tokenization) of the subreddit
    based on an average of all the entries we have for it
    """
    q = list(Entry.select(fn.Avg(Entry.val).alias('avg')).where(Entry.sub == sub))
    return q[0].avg

def get_subs_sorted_polarity():
    """
    Returns a sorted list of tuples (sub_name, sub_polarity) containing
    the information from `get_sub_polarity`.
    """
    return sorted(map(lambda i: (i, get_sub_polarity(i)), get_unique_subs()), key=lambda i: i[1])

# Aggregate functions
def ag_get_sub_polarity_extremes(amount):
    """
    Returns the `amount` number of best and worst subs based on polarity
    """
    base = get_subs_sorted_polarity()
    high, low = zip(*[(base[-(i + 1)], base[i]) for i in range(amount)])
    return high, low

if __name__ == '__main__':
    #print "Unique Subs w/ count:\n %s" % Counter(get_unique_sub_counts())
    polarity = ag_get_sub_polarity_extremes(5)
    print "Best Subreddits: ", polarity[0]
    print "Worst Subreddits:", polarity[1]