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

import json
import sys
import os
config = {}
messages = {}


def init():
    load()
#[16:42] <tosky> e che è, "Frau Blücher" ?
#[16:42] <Straker> Iiiihhh.
#[16:42] <LtWorf> iiiiiiiiiiiiiiiihhhhh
#[16:42] <salvin> hihihih


def save():
    # replace database on disk
    f = file("%s/reacts" % config['files'], 'w')
    json.dump(messages, f)
    f.close()


def load():
    global messages
    f = file("%s/reacts" % config['files'])
    messages = json.load(f)
    f.close()


def sendmsg(source, recip, text):
    if text.startswith(config['control'] + "addreact "):
        react = text.split(" ", 1)[1].strip()
        parts = react.split('#', 1)
        if (len(parts) != 2):
            return "Grazie del tuo contributo %s, nessuno si ricorderà di te" % source
        elif (not parts[1]):
            del messages[parts[0]]
            save()
        else:
            messages[parts[0].lower()] = parts[1]
            save()
        return "Vuoi pure che ti dica grazie? Gli altri ti odieranno per quello che hai fatto."

    text = text.lower()
    values = []
    for k in messages:
        if k in text:
            values.append(messages[k])
    return '\n'.join(values)


def help():
    return config['control'] + "addreact stringa#risposta"
    pass
