# -*- coding: utf-8 -*-
# Relational
# Copyright (C) 2008  Salvo "LtWorf" Tomaselli
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
config={}
messages={}

def init():
    load()
#[16:42] <tosky> e che è, "Frau Blücher" ?
#[16:42] <Straker> Iiiihhh.
#[16:42] <LtWorf> iiiiiiiiiiiiiiiihhhhh
#[16:42] <salvin> hihihih

def append(react):
    f=file("%s/reacts"%config['files'],"a")
    f.write(react)
    f.write("\n")
    f.close()

def load():
    f=file("%s/reacts"%config['files'])
    while True:
        l=f.readline().strip()
        if len(l)==0:
            return
        parts=l.split('#',1)
        messages[parts[0]]=parts[1]
    f.close()

def sendmsg (source,recip,text):
    if text.startswith(config['control']+"addreact "):
        react=text.split(" ",1)[1].strip()
        parts=react.split('#',1)
        if (len(parts)!=2):
            return "Grazie del tuo contributo %s, nessuno si ricorderà di te" % source
        messages[parts[0].lower()]=parts[1]
        react="%s#%s" %(parts[0].lower(),parts[1])
        append(react)
        return "Vuoi pure che ti dica grazie? Gli altri ti odieranno per quello che hai fatto."

    text=text.lower()
    for i in messages:
        if text.rfind(i) != -1:
            return messages[i]
    return None
def help():
    return config['control']+"addreact stringa#risposta"
    pass
