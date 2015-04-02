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

# General stub module for things like praise,beer,cake,insult...

import random
import authorization

larts=[]
config={}
modconfig={}

def init():
    modconfig['file']="general"
    modconfig['good']=True #Defines if it is used for good or bad, if for bad the bot will not do it to itself
    
    load()

def save(lart_list):
    f=file("%s/%s" % (config['files'],modconfig['file']) ,"w")
    for i in lart_list:
        f.write(i)
        f.write("\n")
    f.close()
    pass

def append(lart):
    f=file("%s/%s"%(config['files'],modconfig['file']),"a")
    f.write(sanitize(lart))
    f.write("\n")
    f.close()
    

def load():
    f=file("%s/%s"% (config['files'],modconfig['file']))
    while True:
        l=f.readline().strip()
        if len(l)==0:
            return
        larts.append(l)
    f.close()

def sendmsg (source,dest,text):
    if text.startswith(config['control']+modconfig['file']+" "):
        return perform_action(source,dest,text)
    elif text.startswith(config['control']+"add"+modconfig['file'] + " "):
        return add_to_database(source,dest,text)
    return None

def perform_action(source,dest,text):
    
    if not authorization.check_permissions(perform_action,source,dest,text):
        return None
    
    tok=text.split(' ')
    larted=tok[1].strip()
    if tok[len(tok)-1].strip().isdigit():
        lartid=int(tok[len(tok)-1])
        if lartid>=len(larts):
            lartid=random.randint(0,len(larts)-1)
            larted=source
    else:
        lartid=random.randint(0,len(larts)-1)
    
    
    if modconfig['good']==True and larted==source:
       return "Io non sono il leccapiedi di %s" % source
    elif modconfig['good']==False and larted==config['nickname']:
        larted=source
    return "\001ACTION "+ (larts[lartid] % (larted)) +"\001"
        

def add_to_database(source,dest,text):
    
    if not authorization.check_permissions(add_to_database,source,dest,text):
        return None
    
    
    lart=text.split(" ",1)[1].strip()
    if (len(lart) - len(lart.replace("%s","")) != 2):
        return "Grazie del tuo inutile contributo %s." % source
    larts.append(lart)
    append(lart)
    return "Grazie del tuo gentile contributo con il %s %d..." %(modconfig['file'],len(larts)-1)

    
def help():
    return "%s%s nickname per complimentarsi \\ %sadd%s per aggiungere una nuova frase. Usare %%s per il nickname." % (config['control'],modconfig['file'],config['control'],modconfig['file'])
    pass
