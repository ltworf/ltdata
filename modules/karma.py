# -*- coding: utf-8 -*-
# LtData
# Copyright (C) 2010  Salvo "LtWorf" Tomaselli
#
# Relation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

import sys
import os
config = {}
karma = {}


def init():
    load()


def load():
    f = file("%s/karma" % config['files'])
    while True:
        l = f.readline().strip()
        if len(l) == 0:
            return
        parts = l.split('#', 1)
        karma[parts[0]] = int(parts[1])
    f.close()


def readval(nickname):
    try:
        return karma[nickname]
    except:
        return 0


def save():
    f = file("%s/karma" % config['files'], "w")
    for i in karma:
        f.write("%s#%d" % (i, karma[i]))
        f.write("\n")
    f.close()
    pass


def sendmsg(sender, recip, text):
    text = text.strip()
    if text == (config['control'] + "karma"):
        rank_pos = sorted([(k, n)
                          for n, k in karma.items() if k > 0], reverse=True)[:3]
        rank_neg = sorted([(k, n) for n, k in karma.items() if k < 0])[:3]
        return ("Gli idoli sono %s e gli disgraziati sono %s" %
                (", ".join(["%s(%d)" % (n, k) for (k, n) in rank_pos]),
                 ", ".join(["%s(%d)" % (n, k) for (k, n) in rank_neg])))
    elif text.startswith(config['control'] + "karma "):
        nick = text.split(" ", 1)[1].strip()
        try:
            return "%s: %d" % (nick, karma[nick])
        except:
            return "Ma di che parli?"
    elif (text.endswith('++') and len(text.split(' ')) == 1):
        return vote(text[:-2])
    elif (text.endswith('--') and len(text.split(' ')) == 1):
        return vote(text[:-2], -1)
    return None

def vote(nick, delta=1):
    if nick.lower() == config['nickname'].lower() and delta > 0:
        result = "Grazie per la tua stima"
    elif nick.lower() == config['nickname'].lower() and delta <= 0:
        return "Nah, non credo di volerlo fare"
    elif nick.lower() == sender.lower() and delta > 0:
        return "Un po' autoreferenziale, non credi?"
    else:
        result = "Prendo nota."
    entry = filter(lambda n: n.lower() == nick.lower, karma.keys())
    if entry:
        entry = entry[0]
    else:
        entry = nick
    karma[entry] = readval(entry) + delta
    result = "%s %s: %d" % (result, entry, karma[entry])
    save()
    return result

def help():
    return ".karma per vedere la classifica, .karma nickname per vedere il karma della persona, nickname++ o nickname-- per aumentarlo o diminuirlo"
    pass
