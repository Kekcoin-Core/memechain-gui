import json
import urllib2
from math import ceil

from sightengine.client import SightengineClient


def getJSON(url):
    return json.loads(urllib2.urlopen(urllib2.Request(url), timeout=30).read())


class Pagination(object):
    """A Pagination object to be used for querying and displaying pagination links on frontend

    Example usage:

    >>> p = Pagination(total=15, per_page=5, current_page=1)
    >>> p.start
    0
    >>> p.pages
    [1, 2, 3]
    >>> p.next_page
    2
    >>> p.current_page = 2
    >>> p.prev_page
    1
    >>> p.next_page
    3
    >>> p.start
    5

    :copyright: (c) 2013 James Morris http://jmoz.co.uk.
    """

    def __init__(self, total=None, per_page=100, current_page=1):
        """init with total number of items in your set, how many you want per_page, and set the current_page you are on"""
        self.total = total
        self.per_page = per_page
        self.current_page = current_page

    def __repr__(self):
        return str(self.__dict__)

    @property
    def total_pages(self):
        """The number of pages this pagination can have due to the total and per_page, e.g. total 10, per_page 5 = 2 total_pages
        Cast to float so result is float, round up, then back to int
        """
        return int(ceil(float(self.total) / self.per_page))

    @property
    def pages(self):
        """Returns list of integers of pages e.g. for 3 pages [1,2,3]"""
        return range(1, self.total_pages + 1)

    @property
    def next_page(self):
        """The page number after the current_page or None"""
        return self._get_page_offset(+1)

    @property
    def prev_page(self):
        """The page number before the current_page or None"""
        return self._get_page_offset(-1)

    def _get_page_offset(self, offset):
        """Give an offset, +1 or -1 and the page number around the current_page will be returned
        So if we are on current_page 2 and pass +1 we get 3, if we pass -1 we get 1.  Or None if not valid
        """
        try:
            return self.pages[self.pages.index(self.current_page + offset)]
        except ValueError:
            return None

    @property
    def start(self):
        """The starting offset used when querying"""
        return self.current_page * self.per_page - self.per_page


class MemeTimeline(object):
    api_root = "http://95.179.132.93:1337/api"

    @classmethod
    def find_paginated(self, pagination):
        memechain_height = int(getJSON("%s/getheight" % self.api_root)['result'])
        # self.count returns the total number of items in the timeline
        pagination.total = memechain_height
        # pass in the pagination params which can be used as offset
        timeline = self.find(limit=pagination.per_page, start=pagination.start, memechain_height=memechain_height)
        return timeline

    @classmethod
    def find(self, limit=100, start=0, memechain_height=0):
        sightclient = SightengineClient("1347331372", "BhoFasNuF3zAGp8XSRXi")
        timeline = []

        for ident in range(start, start + limit):
            meme_height = memechain_height - ident
            rawdata_meme = getJSON("%s/getmemedatabyheight/%s" %
                                   (self.api_root, str(meme_height)))['result']

            sight_output = sightclient.check('nudity').set_url(
                'https://ipfs.io/ipfs/%s' % rawdata_meme['ipfs_id'])

            try:
                if sight_output['nudity']['safe'] > 0.5:
                    timeline.append(
                        dict(rawdata_meme, **{'meme_height': meme_height}))
                else:
                    pass

            except KeyError as e:
                timeline.append(
                    dict(rawdata_meme, **{'meme_height': meme_height}))

        return timeline

    @classmethod
    def find_meme(self, meme):
        sightclient = SightengineClient("1347331372", "BhoFasNuF3zAGp8XSRXi")

        try:
            height = int(meme)
            # meme represents height
            rawdata_meme = getJSON("%s/getmemedatabyheight/%s" %
                                   (self.api_root, meme))['result']

        except ValueError as e:
            # meme represents ipfsid
            rawdata_meme = getJSON("%s/getmemedatabyhash/%s" %
                                   (self.api_root, meme))['result']

        sight_output = sightclient.check('nudity').set_url(
            'https://ipfs.io/ipfs/%s' % rawdata_meme['ipfs_id'])

        if sight_output['nudity']['safe'] > 0.5:
            return dict(rawdata_meme,**{'meme_height': self.memechain_height})
        else:
            return None
