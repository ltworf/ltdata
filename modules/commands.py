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
disabled = []


def init():
    pass


def check(sender):
    if sender != config['owner']:
        return "%s, pensi di essere il capitano Picard?" % sender
    return None


def sendmsg(sender, recip, text):
    text = text.rstrip()
    is_admin = check(sender)

    if text.startswith(config['control'] + "enable "):

        if is_admin != None:
            return is_admin

        items = text.split(" ")
        for i in disabled:
            if items[1] == i.__name__.split(".", 1)[1]:
                config['modules'].append(i)
                disabled.remove(i)
                return None
    if text.startswith(config['control'] + "disable "):
        if is_admin != None:
            return is_admin
        # pass
        items = text.split(" ")
        for i in config['modules']:
            if items[1] == i.__name__.split(".", 1)[1]:
                config['modules'].remove(i)
                disabled.append(i)
                return None

    if text.startswith(config['control'] + "quit"):  # quit
        if is_admin != None:
            return is_admin
        sys.exit(1)
    elif (text.startswith(config['control'] + "restart") or text.startswith(config['control'] + "reboot")):
        if is_admin != None:
            return is_admin
        sys.exit(0)
    elif text.startswith(config['control'] + "version"):
        return "E tu %s? Sei ancora una alpha vero?" % sender
    elif text.startswith(config['control'] + "nickname"):  # change nickname
        if is_admin != None:
            return is_admin
        # Change nickname
        try:
            config['nickname'] = text.split(' ')[1]
            config['socket'].send('NICK %s\r\n' % config['nickname'])
        except:
            return "Non riesco a capire il senso della richiesta"
    elif text.startswith(config['control'] + "join"):  # Join channel
        if is_admin != None:
            return is_admin
        try:
            join((text.split(' ')[1],))
        except:
            return "Canale subspaziale troppo disturbato"
    elif text.startswith(config['control'] + "help"):  # help
        items = text.split(" ")
        if len(items) == 1:
            mod = "Moduli caricati: "
            for i in config['modules']:
                mod += i.__name__.split(".", 1)[1] + ' '
            return mod
        else:
            for i in config['modules']:
                if items[1] == i.__name__.split(".", 1)[1]:
                    return i.help()
            return "Di che stai parlando?"


def help():
    return "Questo modulo può essere usato solo dagli ufficiali superiori"
    pass
