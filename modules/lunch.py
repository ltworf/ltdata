import datetime
import httplib
from urlparse import urlparse
# import xml.etree.ElementTree as ET
import defusedxml.ElementTree as ET


class Connection(httplib.HTTPConnection):

    '''
    Same thing as HTTPConnection but
    can be used in a with block
    '''

    def __exit__(self, type, value, traceback):
        self.close()

    def __enter__(self):
        return self


def get_url():
    '''
    Gets the URL of today's feed
    '''
    today = datetime.date.today()
    return 'http://cm.lskitchen.se/johanneberg/karrestaurangen/sv/%04d-%02d-%02d.rss' % (today.year, today.month, today.day)


def get_feed():
    '''
    Reads today's feed and returns the entire body
    '''
    url = urlparse(get_url())

    with Connection(url.netloc) as connection:
        connection.request(
            "GET",
            url.path,
        )

        response = connection.getresponse()
        if response.status != 200:
            raise Exception('Request failed')
        return response.read()


def get_lunch():
    '''
    Returns a list of tuples containing the lunch menu
    '''
    rss = ET.fromstring(get_feed())
    channel = rss.find('channel')

    r = []

    for i in channel.findall('item'):
        title = i.find('title').text
        description = i.find('description').text

        # They tend to end the strings with a weird @number
        if '@' in description:
            description = description.split('@', 1)[0]

        r.append((title, description))
    return r

# BOT interface

config = {}


def init():
    '''
    Some needed interface for the bot
    '''
    pass


def sendmsg(sender, recip, text):
    if text.rstrip() != config['control'] + 'lunch':
        return None

    lunch_list = get_lunch()
    r = '\n'.join(map(lambda x: '%s: %s' % (x[0], x[1]), lunch_list))
    return r.encode('utf-8')


def help():
    return 'Che veleno vuoi oggi?'
