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
from datetime import datetime, timedelta
from collect import collect
import pytz

import matplotlib
matplotlib.use('cairo.png')
import matplotlib.pyplot as plt

def compress_data(data, start, delta):
    plot = []
    data.sort()
    end = start + delta
    count = 0
    for point in data:
        if point < start:
            continue
        while point > end:
            plot.append((start, count))
            end += delta
            start += delta
            count = 0
        if point > start and point < end:
            count += 1
    while start < pytz.utc.localize(datetime.now()):
        plot.append((start, count))
        end += delta
        start += delta
        count = 0
    return plot

def rolling_average(data, count):
    last = [0]*count
    output = []
    for point, value in data:
        last.pop()
        last.insert(0, value)
        output.append((point, float(sum(last))/count))
    return output

def xy(data):
    return ([x[0] for x in data],[y[1] for y in data])

if __name__ == "__main__":
    activity = collect()
    for where in activity:
        print where
        for who in activity[where]:
            print "  %s" % who
            print "    compress data"
            data = compress_data(activity[where][who], pytz.utc.localize(datetime(2002, 1, 1)), timedelta(days=31))
            print "    generate rolling average"
            rlavg = rolling_average(data, 3)
            print "    plot data"
            plt.bar(*xy(data), width=[datetime.min+timedelta(days=30)]*len(data))
            print "    plot rolling average"
            plt.plot(*xy(rlavg), color='red')
            filename = '%s-%s-2002-1m-3m-avg.png' % (where, who.encode('ascii','xmlcharrefreplace'))
            print "    save to %s" % filename
            plt.savefig(filename, transparent=True, bbox_inches='tight')
            plt.close()
