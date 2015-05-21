# LtData
# Copyright (C) 2015 Salvo "LtWorf" Tomaselli
#
# Relation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>


import json
from time import strftime
from os.path import normpath, isdir


maildir = "%s/%s" % (config['files'], 'mail')


def openmbox(name):
    mbox = normpath('%s/%s' % (maildir, name))
    if not mbox.startswith(maildir):
        return None
    try:
        return open(mbox, 'r+')
    except:
        return None


def writembox(index, mboxp):
    mboxp.seek(0)
    json.dump(index, mboxp)
    mboxp.truncate()


def init():
    if not isdir(maildir):
        mkdir(maildir)


def sendmsg(source, dest, text):
    if text.startswith(config['control'] + "mail"):
        # read
        if ' ' not in text:
            mboxp = openmbox(source)
            if not mboxp:
                return "mail: no such mailbox"
            with mboxp:
                index = json.load(mboxp)
                if index:
                    writembox([], mboxp)
                    return '\n'.join(['On %s, %s said: %s' %
                                      (m['Date'], m['From'], m['Body'])
                                      for m in index])
                else:
                    return "mail: no new messages"
        # send
        else:
            args = text.split(' ', 2)
            if len(args) < 2:
                return "mail: message must not be empty"
            _, mbox, msg = args
            mboxp = openmbox(mbox)
            if not mboxp:
                return "mail: no such mailbox"
            with mboxp:
                index = json.load(mboxp)
                if len(index) >= 50:
                    return "mail: mailbox full"
                index.append({'From': source,
                              'Date': strftime("%Y-%m-%d %H:%M:%S"),
                              'Body': msg.strip()})
                writembox(index, mboxp)
                return "mail: mail sent."


def help():
    return '\n'.join([config['control'] + "mail: empty mailbox and read mail",
                      config['control'] + "mail <mbox> <msg>: " +
                      "put the given message in the specified mailbox"])
