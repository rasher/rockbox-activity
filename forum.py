#!/usr/bin/env python
# vim: set fileencoding=UTF-8 :
#
# Copyright (c) 2010, Jonas Häggqvist <rasher@rasher.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the program nor the names of its contributors may be
#   used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
    if OPENER == None:
        url = "http://forums.rockbox.org/index.php?action=login2"
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
        formdata = {'passwrd':passwrd, 'hash_passwd':'', 'user':user}
        opener.open(url, urllib.urlencode(formdata)).read()
        OPENER = opener


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
        data = OPENER.open(url).read()

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
    user = 'Rockbox'
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: %s user password" % sys.argv[0]
        sys.exit(1)
    names = staff()
    login(sys.argv[1], sys.argv[2])
    if user not in names:
        print >> sys.stderr, "Something's wrong: %s is not in staff" % user
        sys.exit(2)
    posts = userposts(names[user])
    if len(posts) < 1:
        print >> sys.stderr, "Something's wrong: No posts found for %s" % user
        sys.exit(3)
