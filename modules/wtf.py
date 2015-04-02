# -*- coding: utf-8 -*-

# LtData
# Copyright (C) 2009  Salvo "LtWorf" Tomaselli
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

import os
config={}
def init():
    pass

def sendmsg (source,dest,text):
    if text.startswith(config['control']+"wtf"):
        p=text.strip().split(' ')
        if len(p)==1:
            return
        f=os.popen("wtf %s" % p[1].upper())
        res=f.read().rstrip().replace("\n","\\ ")
        return res
    return None
def help():
    return config['control']+"wtf sigla per ottenere il significato"
    pass
