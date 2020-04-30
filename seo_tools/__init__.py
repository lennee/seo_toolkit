import asyncio

from seo_tools._lighthouse import LighthouseReport
from seo_tools._gt_metrix import GTMetrix
from seo_tools._moz import moz_single, moz_batch
from seo_tools.generic import _cdn, _domain_age, _http2, _https, _mobile_friendly, _pagespeed, _lighthouse
from seo_tools._google_search import search
from seo_tools.utils import batch

from functools import partial
from concurrent.futures import ThreadPoolExecutor

def lighthouse(url, **kwargs):
    '''
        Runs a lighthouse audit of a given url or list of urls

        Example:

            In [1]:    from seo_tools import lighthouse

                       lh = lighthouse('https://www.example.com')

                       lh.mobile.score

            Out [1]:   9

        Args:

            url (str or list): A url or list of urls to be audited

        Kwargs:

            strategy (str): strategy for the audit to
                be run as. If none is given, both mobile and desktop
                will be run.

                    Options: 'mobile' || 'desktop'

            category (str or list): category or list of categories for
                audit to be run as. If none is given, a full audit is run.

                    Options: 'accessibility' || 'best-practices'
                               || 'performance' || 'pwa' || 'seo'

        Returns:

            Single Lighthouse object or a list of
                Lighthouse objects.

            Documentation on the Lighthouse object can be found under
                the _lighthouse.py file
    '''

    strategy = kwargs.get('strategy') if 'strategy' in kwargs else None
    if isinstance(url, str):
        return asyncio.run(_lighthouse(url, strategy=strategy))
    elif isinstance(url, list):
        return asyncio.run(batch(_lighthouse, url, strategy=strategy))

def mobile_friendly(url):
    '''
        Runs a Mobile Friendly test of a given url or list of urls

        Example:

            In [1]:    from seo_tools import mobile_friendly

                       mf = mobile_friendly('https://www.example.com')

                       mf.mobileFriendliness

            Out [1]:   MOBILE_FRIENDLY

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Single MobileFriendly object or a list of
                MobileFriendly objects.

            Documentation on the MobileFriendly object can be found under
                the _mobile_friendly.py file
    '''

    if isinstance(url, str):
        return asyncio.run(_mobile_friendly(url, strategy=strategy))
    elif isinstance(url, list):
        return asyncio.run(batch(_mobile_friendly, url, strategy=strategy))

def gt_metrix(url):
    '''
        Runs a GT Metrix test of a given url or list of urls

        Example:

            In [1]:    from seo_tools import gt_metrix

                       gtm = gt_metrix('https://www.example.com')

                       gtm.yslow_score

            Out [1]:   58

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Single GTMetrix object or a list of
                GTMetrix objects.

            Documentation on the GTMetrix object can be found under
                the _gt_metrix.py file
    '''
    return run(GTMetrix, url)

def moz(url, cols=103079215104):
    '''
        Runs a MozScapes API call of a given url or list of urls for the
            specified parameters.

        Example:

            In [1]:    from seo_tools import moz

                       m = moz('https://www.example.com')

                       m.da

            Out [1]:   80

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Single Moz Object

            Documentation on the Moz object can be found under
                the _moz.py file
    '''
    if isinstance(url, str):
        return asyncio.run(moz_single(url))
    elif isinstance(url, list):
        return asyncio.run(moz_batch(url))

def cdn(url):
    '''
        Fetches CDN for a given url or list of urls

        Example:

            In [1]:    from seo_tools import cdn

                       cdn('https://www.example.com')

            Out [1]:   'INSTARTLOGIC-NET2'

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            CDN or a list of CDN's (str, list(str))
    '''
    if isinstance(url, str):
        return _cdn(url)
    elif isinstance(url, list):
        return [_cdn(u) for u in url]

def domain_age(url):
    '''
        Fetches the domain age for a given url or list of urls

        Example:

            In [1]:    from seo_tools import domain_age

                       domain_age('https://www.example.com')

            Out [1]:   datetime.datetime

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Domain Creation Date or a list of Domain Creation Dates
                (datetime.datetime, list(datetime.datetime))
    '''
    if isinstance(url, str):
        return _domain_age(url)
    elif isinstance(url, list):
        return [_domain_age(u) for u in url]

def http2(url):
    '''
        Determines if the given url or list of urls supports the HTTP/2
            Protocol

        Example:

            In [1]:    from seo_tools import http2

                       http2('https://www.example.com')

            Out [1]:   True

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Supports HTTP/2? or list of support as (boolean || list(boolean))
    '''
    if isinstance(url, str):
        return _http2(url)
    elif isinstance(url, list):
        return [_http2(u) for u in url]

def https(url):
    '''
        Determines if the given url or list of urls supports the HTTPS
            Protocol

        Example:

            In [1]:    from seo_tools import https

                       https('https://www.example.com')

            Out [1]:   True

        Args:

            url (str or list): A url or list of urls to be tested

        Returns:

            Supports HTTPS? or list of support as (boolean || list(boolean))
    '''
    if isinstance(url, str):
        return asyncio.run(_https(url))
    elif isinstance(url, list):
        return asyncio.run(batch(_https, url))

def google_search(q, num=100):
    '''
        Runs a google search and returns a Pandas DataFrame of the results
            (Rank as int, Title as str, link as str, and domain as str)

        Example:

            In [1]:    from seo_tools import google_search

                       google_search('facebook')

            Out [1]:   DataFrame

        Args:

            keyword (str or list): A search query or list of queriess to
                be searched

        Returns:

            Search Results Pandas.DataFrame or list(Pandas.DataFrame)

        ToDo:

            Make more robust
    '''
    return run(search, q, num=100)

def pagespeed(url, **kwargs):
    strategy = kwargs.get('strategy') if 'strategy' in kwargs else None
    if isinstance(url, str):
        return asyncio.run(_pagespeed(url, strategy=strategy))
    elif isinstance(url, list):
        return asyncio.run(batch(_pagespeed, url, strategy=strategy))
