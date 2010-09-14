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
import urllib2
from os import unlink
from glob import glob
from datetime import datetime
from os.path import exists, join, basename

def update(mldir):
    fpurl = 'http://www.rockbox.org/mail/'
    frontpage = urllib2.urlopen(fpurl).read()

    # Always update the current and previous month
    # If this script is run less than once per month, you may end up with a
    # half-finished month
    now = datetime.now().timetuple()[0:2]
    lastmonth = datetime.now().replace(month=datetime.now().month-1).timetuple()[0:2]
    for curmonth in glob(mldir + '/*%04d-%02d*.html' % now) + glob(mldir + '/*%04d-%02d*.html' % lastmonth):
        unlink(curmonth)
    for archive in re.findall(r'archive/rockbox-.*archive-\d\d\d\d-\d\d', frontpage):
        source = "http://www.rockbox.org/mail/%s" % archive
        target = join(mldir, basename(archive) + '.html')
        if not exists(target):
            f = open(target, 'w')
            f.write(urllib2.urlopen(source).read())
            f.close()
    
def getactivity(mldir, userlist):
    activity = {}
    namemap = {}
    search = re.compile(r'(?i)<em>\s*(?P<author>[^<]*?)\s*</em>.*?<em>\((?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\)</em>')
    sweden = pytz.timezone('Europe/Stockholm')
    for user in userlist:
        if 'ml' not in userlist[user]:
            continue
        for usedname in userlist[user]['ml']:
            namemap[usedname] = user
    for month in glob(mldir + '/*.html'):
        data = open(month).read().decode('Latin-1')
        for m in search.finditer(data):
            if m.group('author') in namemap:
                realname = namemap[m.group('author')]
                if realname not in activity:
                    activity[realname] = []
                activity[realname].append(
                        sweden.localize(datetime(*map(int, m.group('y','m','d')))).astimezone(pytz.utc)
                        )

    return activity

if __name__ == "__main__":
    users = {
            'Jonas Häggqvist': {
                'ml': [u'Jonas Häggqvist', 'Jonas H'],
                    },
                }
    mldir = 'ml'
    update(mldir)
    activity = getactivity(mldir, users)
    for user in activity:
        print "%s: %d" % (user, len(activity[user]))
