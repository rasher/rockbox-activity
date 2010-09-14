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
from people import people
import forum
import irc
import svn
import ml

def config(v):
    c = dict([x.split(':') for x in open('config').readlines()])
    return c[v].strip()

if __name__ == "__main__":
    mldir = 'ml'
    irclogs = 'irclogs'
    svnrevs = 'svnrevs'
    ml.update(mldir)
    irc.update(irclogs)
    forum.login(config('forumuser'), config('forumpass'))
    
    activity = {
            'ml': ml.getactivity(mldir, people),
            'IRC' : irc.getactivity(irclogs, people),
            'SVN' : svn.getactivity(svnrevs, people),
            'Forum': forum.getactivity(people),
    }
    units = {
            'ml':'mail',
            'IRC':'line',
            'SVN':'commit',
            'Forum':'post',
            }
    for user in people:
        print user
        for loc in activity:
            if user in activity[loc]:
                count = len(activity[loc][user])
                unit = units[loc]
                s = "s"
                if unit == 1:
                    s = ""
                print "  %s%s %s%s" % (loc.ljust(7, '.'), str(count).rjust(7, '.'), unit, s)
