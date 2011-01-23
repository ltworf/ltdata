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
import pickle
import time

config={}
seen={}
modconfig={}


def init():
    modconfig['counter']=0
    load()
    pass

def load():
    try:
        seen=pickle.load(open("%s/seen"%config['files'],'rb'))
    except:
        seen={}

def save():
    pickle.dump(seen,open("%s/seen"%config['files'],'wb'))

def sendmsg (sender,recip,text):
    text=text.rstrip()

    #store the last message of the user
    seen[sender]=time.ctime()

    #saves the status each 500 messages, to don't keep the disk too busy
    modconfig['counter']+=1
    if modconfig['counter']>=5: #500:
        save()
        modconfig['counter']=0

    #respond to the request
    if text.startswith(config['control']+"seen "):
        nick=text.split(" ",1)[1]
        try:
            return "%s ha scritto %s" % (nick,seen[nick])
        except:
            return "Non ho visto %s" % nick
    #    return result
    return None
def help():
    return "%sseen nickname per vedere quando la persona ha scritto l'ultima volta" % config['control']
    pass
