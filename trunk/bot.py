#!/usr/bin/python
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


import socket
import sys

#Importing plugins
import modules
from modules import *

modules_list=[] #List containing all the functions of modules
config={}

def sendmsg (sock,dest,text):
    '''Sends a message to a room or a person'''
    sock.send( 'PRIVMSG %s :%s\r\n'%(dest,text) )

def reply (sender,recip,text,sock):
    '''Called when there is an incoming message,
    returns the eventual reply or none'''
    for i in modules_list:
        r=i.sendmsg(sender,recip,text)
        print "MODULE %s(%s,%s,%s) replied %s" %(str(i),sender,recip,text,r)

        if r!=None:
            #Determinig if message was to a room or a private one
            if (not recip.startswith('#')):
                recip=sender
            print "Replying" , r
            for i in r.split("\n"):
                sendmsg(sock,recip,i)
    return None

def join (sock,channels):
    '''Joins a list of channels'''
    for i in channels:
        print "Joining channel: %s" % i
        sock.send ( 'JOIN %s\r\n' % i )

def sanitize(a,splits=1):
    b=a.split("%s",splits)
    a=""
    for i in b:
        a+=i.replace("%","%%")+"%s"
    return a[:-2]


config['modules'] = modules_list

try:
    execfile(sys.argv[1])
except:
    config['network'] = 'calvino.freenode.net' #'irc.as.azzurra.org'#'irc.freenode.net'
    config['port'] = 6667
    config['nickname'] = "LtData"
    config['channels'] = ('#debian-it','#debian-scn') #"#dmi"
    config['owner'] = "LtWorf"
    config['control']="."

sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

for i in modules.__all__:
    print "Adding module: ", i
    mod=eval(i)
    mod.config=config
    mod.sanitize=sanitize
    mod.init()
    modules_list.append(mod) #Adding module to the list


sock.connect ( ( config['network'], config['port'] ) )
#print sock.recv ( 4096 )
print "Connected..."
sock.send ( 'NICK %s\r\n' % config['nickname'] )
sock.send ( 'USER %s PyIRC PyIRC :LtData che usa un dispositivo LCARS\r\n' % config['nickname'] )
join(sock,config['channels'])

for i in config['channels']:
    sendmsg(sock,i,"%s online" % config['nickname'])

while True:
    data = sock.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
        print "Sending: ",('PONG ' + data.split() [ 1 ])
        sock.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    elif data.find ( 'PRIVMSG' ) != -1:
        nick = data.split ( '!' ) [ 0 ].replace ( ':', '' )
        message = ':'.join ( data.split ( ':' ) [ 2: ] )
        try:
            destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]
        except:
            destination = ""
        print '(', destination, ')', nick + ':', message
        reply(nick,destination,message,sock)
