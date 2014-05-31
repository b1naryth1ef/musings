import requests, sys, textblob, time, sys
from database import Entry

def poll_recent_comments():
    last = None
    while True:
        r = requests.get("http://api.redditanalytics.com/searchRecentComments")
        data = r.json()

        for obj in data['data']:
            if obj['id'] == last:
                break
            yield obj

        last = data['data'][0]['id']
        time.sleep(1)

def parse_single(comment):
    blob = textblob.TextBlob(comment)
    avg = 0
    for sentence in blob.sentences:
        avg += sentence.sentiment.polarity
    return avg

if __name__ == '__main__':
    parsed = 0
    for item in poll_recent_comments():
        parsed += 1
        e = Entry()
        e.sub = item['subreddit']
        e.val = parse_single(item['body'])
        e.cid = item['id']
        e.body = item['body']
        e.ups = item['ups']
        e.downs = item['downs']
        e.link_url = item['link_url']
        e.link_title = item['link_title']
        e.author = item['author']
        e.save()
        if parsed % 10 == 0:
            print "Parsed %s comments..." % parsed

        if parsed >= 5000000:
            sys.exit()