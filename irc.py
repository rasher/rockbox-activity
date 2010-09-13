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
from glob import iglob
from datetime import datetime
from os.path import basename, join, exists

def downloadnew(todir):
    url = "http://www.rockbox.org/irc/"
    data = urllib2.urlopen(url).read()
    for loglink in re.findall(r'log-\d{8}', data):
        log = "http://www.rockbox.org/irc/rockbox-%s.txt" % loglink.replace('log-', '')
        target = join(todir, basename(log))
        if not exists(target):
            print "Getting %s" % target
            f = open(target, 'w')
            f.write(urllib2.urlopen(log).read())
            f.close()

def getactivity(fromdir, userlist):
    l = re.compile(r'^(?P<h>\d\d)\.(?P<m>\d\d).(?P<s>\d\d) \#\s*<(?P<nick>[^>]*)>')
    activity = {}
    sweden = pytz.timezone('Europe/Stockholm')
    for logfile in iglob("%s/rockbox-*.txt" % fromdir):
        logdate = [int(logfile[-12:-8]), int(logfile[-8:-6]), int(logfile[-6:-4])]
        for line in open(logfile).readlines():
            m = l.match(line)
            if m:
                for user in userlist:
                    for nickused in userlist[user]['irc']:
                        save = False
                        try:
                            if nickused.match(m.group('nick')):
                                save = True
                        except AttributeError as e:
                            if nickused == m.group('nick'):
                                save = True
                        if save:
                            if user not in activity:
                                activity[user] = []
                            time = datetime(*logdate + map(int, m.group('h','m','s')))
                            time = sweden.localize(time).astimezone(pytz.utc)
                            activity[user].append(time)
    return activity

if __name__ == "__main__":
    users = {
            'Jonas Häggqvist': {
                'irc': [re.compile(r'(?i)rasher.*')],
                    },
                }
    activity = getactivity('irclogs', users)
    for user in activity:
        print "%s: %d" % (user, len(activity[user]))
