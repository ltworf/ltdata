#!/usr/bin/python
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


import socket
import sys

# Importing plugins
import modules
from modules import *

modules_list = []  # List containing all the functions of modules
config = {}


def privmsg(receiver, text):
    '''RFC 1459 PRIVMSG private messages

    Send the message <text> to the channel or nickname <receiver>.

    Bot must be connected.'''
    sendmsg(config['socket'], receiver, text)


def sendmsg(sock, dest, text):
    '''Sends a message to a room or a person'''
    if sock.send('PRIVMSG %s :%s\r\n' % (dest, text)) == 0:
        raise Exception("connection")


def reply(sender, recip, text, sock):
    '''Called when there is an incoming message,
    returns the eventual reply or none'''
    for i in modules_list:
        r = i.sendmsg(sender, recip, text.decode('utf-8'))
        if isinstance(r, unicode):
            r = r.encode('utf-8')

        if r != None:
            # Determinig if message was to a room or a private one
            if (not recip.startswith('#')):
                recip = sender
            print "Replying", r
            for i in r.split("\n"):
                sendmsg(sock, recip, i)
    return None


def onjoin(nick, channel):
    '''Called when a nickname joins one of the channels
    that the bot is participating in.
    
    The main loop handles RFC 1459 JOIN messages by calling
    this method which forwards the event to each module that
    defines an `onjoin` method.'''
    for i in modules_list:
        try:
            i.onjoin(nick, channel)
        except AttributeError:
            pass


def onnick(oldnick, newnick):
    '''Called when a user changes her nickname in one of the
    channels that the bot is participating in.
    
    The main loop handles RFC 1459 NICK messages by calling
    this method which forwards the event to each module that
    defines an `onjoin` method.'''
    for i in modules_list:
        try:
            i.onnick(oldnick, newnick)
        except AttributeError:
            pass


def join(channels):
    '''Joins a list of channels'''
    for i in channels:
        print "Joining channel: %s" % i
        config['socket'].send('JOIN %s\r\n' % i)


def sanitize(a, splits=1):
    b = a.split("%s", splits)
    a = ""
    for i in b:
        a += i.replace("%", "%%") + "%s"
    return a[:-2]


def loadconf():
    '''Loads configuration into the global dictionary: config'''
    config['modules'] = modules_list

    try:
        execfile(sys.argv[1])
    except:
        config[
            'network'] = 'calvino.freenode.net'  # 'irc.as.azzurra.org'#'irc.freenode.net'
        config['port'] = 6667
        config['nickname'] = "LtData"
        config['channels'] = ('#debian-it', '#debian-scn')  # "#dmi"
        config['owner'] = "LtWorf"
        config['control'] = "."


def timeout_recv(sock, size):
    sock.settimeout(3.0)
    try:
        data = sock.recv(size)
        sock.settimeout(None)
        return data
    except:
        sock.settimeout(None)
        return None


def loadmodules():
    for i in modules.__all__:
        print "Adding module: ", i
        mod = eval(i)
        mod.config = config
        mod.sanitize = sanitize
        mod.join = join
        mod.privmsg = privmsg
        mod.init()
        modules_list.append(mod)  # Adding module to the list


def setnickname(sock, nickname):
    sock.send('NICK %s\r\n' % nickname)
    sock.send('USER %s PyIRC PyIRC :LtData che usa un dispositivo LCARS\r\n' %
              nickname)
    data = timeout_recv(sock, 4096)


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config['network'], config['port']))
    config['socket'] = sock

    # print sock.recv ( 4096 )
    print "Connected..."

    data = timeout_recv(sock, 40096)
    # print data

    setnickname(sock, config['nickname'])

    join(config['channels'])

    for i in config['channels']:
        sendmsg(sock, i, "%s online" % config['nickname'])

    while True:
        data = sock.recv(4096)

        if len(data) == 0:  # Disconnected, exit
            return

        if data.find('PING') != -1:
            print "Sending: ", ('PONG ' + data.split()[1])
            sock.send('PONG ' + data.split()[1] + '\r\n')
        elif data.find('PRIVMSG') != -1:
            nick = data.split('!')[0].replace(':', '')
            message = ':'.join(data.split(':')[2:])
            try:
                destination = ''.join(
                    data.split(':')[:2]).split(' ')[-2]
            except:
                destination = ""
            print '(', destination, ')', nick + ':', message
            reply(nick, destination, message, sock)
        elif data.find('JOIN') != -1:
            nick, _, channel = data.split(' ', 3)
            nick = nick.split('!')[0].replace(':', '')
            onjoin(nick, channel)
        elif data.find('NICK') != -1:
            oldnick, _, newnick = data.split(' ', 3)
            oldnick = oldnick.split('!')[0].replace(':', '').strip()
            newnick = newnick.split('!')[0].replace(':', '').strip()
            onnick(oldnick, newnick)

if __name__ == '__main__':
    loadconf()
    loadmodules()

    while(True):
        main()
