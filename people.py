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

people = {
        u'Jonas Häggqvist': {
            'ml': [u'Jonas Häggqvist', 'Jonas H'],
            'irc': ['rasher', 'rasher_', re.compile('(?i)rasher.*'), re.compile('(?i)bacon_.*')],
            'svn': ['rasher'],
            'forum': ['rasher'],
            },
        }

def checkpeople():
    global people
    import urllib2
    url = "http://svn.rockbox.org/viewvc.cgi/trunk/docs/COMMITTERS"
    for line in urllib2.urlopen(url).readlines():
        committer, realname = line.decode('cp1252').strip().split(" ", 1)
        if realname in people:
            if 'svn' not in people[realname] or committer not in people[realname]['svn']:
                print "Add %s to %s" % (committer, realname)

if __name__ == "__main__":
    checkpeople()
