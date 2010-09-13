#!/usr/bin/env python
import re
import pytz
import urllib
import urllib2
import cookielib
from pprint import pprint
from datetime import datetime

OPENER = None

def staff():
    url = "http://forums.rockbox.org/index.php?action=staff"
    data = urllib2.urlopen(url).read()

    # For my next trick, I'll parse HTML with a regexp. Hold my beer
    devs = re.compile(r'<a[^>]*href="[^"]*u=(?P<userid>\d+)[^"]*"[^>]*>\s*<[^>]*>\s*(?P<forumname>[^<]*)')
    return dict([m.group('forumname', 'userid') for m in devs.finditer(data)])

def login(user, passwrd):
    global OPENER
    opener = None
    if OPENER == None:
        url = "http://forums.rockbox.org/index.php?action=login2"
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
        formdata = {'passwrd':passwrd, 'hash_passwd':'', 'user':user}
        opener.open(url, urllib.urlencode(formdata)).read()
        OPENER = opener
    return OPENER


def userposts(userid):
    global OPENER
    if OPENER == None:
        raise Exception("Not logged in") 

    urlf = "http://forums.rockbox.org/index.php?action=profile;u=%d;sa=showPosts;start=%d"
    start = 0
    dates = re.compile(r'<td[^>]*class="middletext"[^>]*>\s*on: (\d\d\d\d)-(\d\d)-(\d\d), (\d\d):(\d\d):(\d\d)')
    posts = []
    lastdate = None
    stop = False
    central = pytz.timezone('US/Central')
    while True:
        url = urlf % (int(userid), start)
        data = opener.open(url).read()

        for date in [datetime(*map(int, m.groups())) for m in dates.finditer(data)]:
            date = central.localize(date).astimezone(pytz.utc)
            if lastdate != None and lastdate <= date: # A date we've seen already
                stop = True
                break 
            posts.append(date)
            lastdate = date
        start += 15
        if stop:
            break
    return posts


if __name__ == "__main__":
    import sys
    names = staff()
    user = 'Rockbox'
    if user not in names:
        print "Something's wrong: %s is not in staff" % user
        sys.exit(1)
    posts = userposts(names[user])
    if len(posts) < 1:
        print "Something's wrong: No posts found for %s" % user
        sys.exit(2)
