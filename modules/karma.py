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
import json
config = {}
karma = {}


def init():
    load()


def load():
    global karma
    f = file("%s/karma" % config['files'])
    karma = json.load(f)
    f.close()


def readval(nickname):
    try:
        return karma[nickname.lower()]
    except:
        return (nickname, 0)


def save():
    f = file("%s/karma" % config['files'], "w")
    json.dump(f)
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
        nick = text[:-2]
        if nick.lower() == sender.lower():
            return "Un po' autoreferenziale, non credi?"
        else:
            return vote(nick)
    elif (text.endswith('--') and len(text.split(' ')) == 1):
        nick = text[:-2]
        if nick.lower() == config['nickname'].lower() and delta <= 0:
            return "Nah, non credo di volerlo fare"
        else:
            return vote(nick, -1)
    return None

def vote(nick, delta=1):
    if nick.lower() == config['nickname'].lower() and delta > 0:
        result = "Grazie per la tua stima"
    else:
        result = "Prendo nota."
    r, k = readval(nick)
    k_ = k + delta
    karma[nick.lower()] = (r, k_)
    result = "%s %s: %d" % (result, r, k_)
    save()
    return result

def help():
    return ".karma per vedere la classifica, .karma nickname per vedere il karma della persona, nickname++ o nickname-- per aumentarlo o diminuirlo"
    pass
