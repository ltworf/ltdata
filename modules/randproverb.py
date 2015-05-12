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

import httplib
import urllib
import json

larts = []
config = {}


def init():
    pass


def query_google_translate(query_string):

    query_string = urllib.quote(query_string)  # Adds escapes

    # Query string
    query_string = "/language/translate/v2?key=%s&q=%s&source=ar&target=it" % (
        config['googlekey'], query_string)

    h1 = httplib.HTTPSConnection('www.googleapis.com')

    h1.connect()
    h1.request("GET", query_string)
    response = h1.getresponse()

    print json.load(response)
    # response.read()


def sendmsg(source, dest, text):
    if text.startswith(config['control'] + "randproverb"):
        try:
            p = text.split(' ', 1)
            return query_google_translate(p[1])
        except:
            pass
    return None


def help():
    return config['control'] + "randproverb testo per ottenere un proverbio strampalato"
    pass
