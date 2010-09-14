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

import pytz
import pysvn
from os.path import exists
from datetime import datetime

def readrevs(svnfile):
    revs = []
    if exists(svnfile):
        for line in open(svnfile).readlines():
            revs.append(line.strip().split(":"))
    return revs

def getactivity(svnfile, userlist):
    activity = {}
    client = pysvn.Client()
    repo = 'svn://svn.rockbox.org/rockbox/trunk'
    namemap = {}
    for realname in userlist:
        for nick in userlist[realname]['svn']:
            namemap[nick] = realname

    revs = readrevs(svnfile)
    if len(revs) > 0:
        fromrev = pysvn.Revision(pysvn.opt_revision_kind.number, revs[-1][0])
    else:
        fromrev = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
    savedrevs = open(svnfile, 'a')
    logs = client.log(repo, revision_end=fromrev)
    logs.reverse()
    for rev in logs:
        if rev.has_key('author') and rev.has_key('date') and rev.has_key('revision') and rev.revision.number > fromrev.number:
            revs.append((rev.revision.number, rev.date, rev.author))
            line = "%s:%f:%s\n" % (rev.revision.number, rev.date, rev.author)
            savedrevs.write(line)

    for rev, timestamp, author in revs:
        if author not in namemap:
            continue
        realname = namemap[author]
        if realname not in activity:
            activity[realname] = []
        activity[realname].append(pytz.utc.localize(datetime.utcfromtimestamp(float(timestamp))))
    return activity

if __name__ == "__main__":
    users = {
            'Jonas Häggqvist': {
                'svn': ['rasher', 'Buschel', 'buschel'],
                    },
                }
    svnfile = 'svnrevs'
    activity = getactivity(svnfile, users)
    for user in activity:
        print "%s: %d" % (user, len(activity[user]))
