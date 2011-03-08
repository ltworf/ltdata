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

import os
import authorization

larts=[]
config={}
def init():
    pass

def sendmsg (source,dest,text):
    
    if not authorization.check_permissions(sendmsg,source,dest,text):
        return None
    
    
    if text.startswith(config['control']+"fortune"):
        f=os.popen("fortune -s")
        return f.read(3000).rstrip().replace("\n","\\ ")
    return None
def help():
    return config['control']+"fortune per ottenere un fortune a caso"
    pass
