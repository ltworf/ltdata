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

import random
larts=[]
config={}
def init():
    load()
def save(lart_list):
    f=file("%s/thanks" %config['files'] ,"w")
    for i in lart_list:
        f.write(i)
        f.write("\n")
    f.close()
    pass

def append(lart):
    f=file("%s/thanks"%config['files'],"a")
    f.write(sanitize(lart))
    f.write("\n")
    f.close()
    

def load():
    f=file("%s/thanks"%config['files'])
    while True:
        l=f.readline().strip()
        if len(l)==0:
            return
        larts.append(l)
    f.close()
def sendmsg (source,dest,text):
    if text.startswith(config['control']+"grazie ") or text.startswith(config['control']+"thanks ") or text.startswith(config['control']+"ringrazia "):
        tok=text.split(' ')
        larted=tok[1].strip()
        if tok[len(tok)-1].strip().isdigit():
            lartid=int(tok[len(tok)-1])
            if lartid>=len(larts):
                lartid=random.randint(0,len(larts)-1)
                larted=source
        else:
            lartid=random.randint(0,len(larts)-1)
        
        if larted==source:
           return "Io non sono il leccapiedi di %s" % source
        return "\001ACTION " + (larts[lartid] % (larted)) + "\001"
    elif text.startswith(config['control']+"addthanks "):
        lart=text.split(" ",1)[1].strip()
        if (len(lart) - len(lart.replace("%s","")) != 2):
            return "Grazie del tuo inutile contributo %s." % source
        larts.append(lart)
        append(lart)
        return "Grazie del tuo gentile contributo con il grazie %d..." %(len(larts)-1)
    return None
def help():
    return "%sgrazie nickname per complimentarsi \\ %saddthanks per aggiungere un complimento. Usare %s per il nickname." % (config['control'],config['control'],"%s")
    pass
