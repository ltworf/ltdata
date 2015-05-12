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

import authorization
import random
larts = []
config = {}


def init():
    load()


def save(lart_list):
    print "saving larts", lart_list
    f = file("%s/larts" % config['files'], "w")
    for i in lart_list:
        f.write(i)
        f.write("\n")
    f.close()
    pass


def append(lart):
    print "appending lart", lart
    f = file("%s/larts" % config['files'], "a")
    f.write(sanitize(lart, 2))
    f.write("\n")
    f.close()


def load():
    f = file("%s/larts" % config['files'])
    while True:
        l = f.readline().strip()
        if len(l) == 0:
            return
        larts.append(l)
    f.close()


def sendmsg(source, dest, text):
    if text.startswith(config['control'] + "lart "):
        return perform_action(source, dest, text)
    elif text.startswith(config['control'] + "addlart "):
        return add_to_database(source, dest, text)
    return None


def add_to_database(source, dest, text):

    if not authorization.check_permissions(add_to_database, source, dest, text):
        return None

    lart = text.split(" ", 1)[1].strip()
    if (len(lart) - len(lart.replace("%s", "")) != 4):
        return "Grazie del tuo contributo %s, nessuno si ricorderà di te" % source
    larts.append(lart)
    append(lart)
    return "Grazie del tuo contributo, i posteri ti ricorderanno grazie al lart %d" % (len(larts) - 1)


def perform_action(source, dest, text):

    if not authorization.check_permissions(perform_action, source, dest, text):
        return None

    tok = text.split(' ')
    larted = tok[1].strip()
    if tok[len(tok) - 1].strip().isdigit():
        lartid = int(tok[len(tok) - 1])
        if lartid >= len(larts):
            lartid = random.randint(0, len(larts) - 1)
            larted = source
    else:
        lartid = random.randint(0, len(larts) - 1)

    if larted == config['nickname']:
        deny = "non "
    else:
        deny = ""
    return "\001ACTION " + (larts[lartid] % (deny, larted)) + "\001"


def help():
    return "%slart nickname per lartare qualcuno \\ %saddlart per aggiungere un lart. Usare due %%s. Il primo per il 'non ' ed il secondo per il nickname. Non usare lo spazio dopo il primo %%s" % (config['control'], config['control'])
    pass
