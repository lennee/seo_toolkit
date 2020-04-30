import asyncio
import socket
import whois
import logging
import requests

from ipwhois import IPWhois
from hyper import HTTP20Connection

from seo_tools.utils import get, clean_url
from seo_tools._lighthouse import LighthouseReport



def _cdn(url):
    '''
        Fetches the cdn of a url

        Ths function serves as the function run by the shell within the
            '__init__.py' file of this module. To run multiple tests concurrently,
            send a list of urls to the 'cdn' function found there.

        Example:

            In [1]:    from seo_tools.generic import _domain_age

                       _cdn('https://www.example.com')

            Out [1]:   'INSTARTLOGIC-NET2'

        Attributes:

            url (str): A url whose cdn is to be fetched.

        Returns:

            cdn (str): A string that defined the cdn of the provided url
    '''

    try:
        url = 'www.' + clean_url(url)
        res = socket.gethostbyname(url)
        obj = IPWhois(res).lookup_whois()
        return obj['nets'][0]['name']
    except:
        return None

def _domain_age(url):
    '''
        Fetches Datetime object of the creation date of the domain

        Ths function serves as the function run by the shell within the
            '__init__.py' file of this module. To run multiple tests concurrently,
            send a list of urls to the 'domain_age' function found there.

        Example:

            In [1]:    from seo_tools.generic import _domain_age

                       _domain_age('https://www.example.com')

            Out [1]:   datetime.datetime(1997, 10, 18, 4, 0)

        Attributes:

            url (str): A url whose domain age is to be fetched.

        Returns:

            Domain Creation Date (datetime.datetime):
                A string that defined the cdn of the provided url
    '''

    try:
        w = whois.whois(url)
        return w.creation_date
    except:
        return None

def _http2(url):
    '''
        Determines if a given url supports HTTP/2 protocol

        Ths function serves as the function run by the shell within the
            '__init__.py' file of this module. To run multiple tests concurrently,
            send a list of urls to the 'http2' function found there.

        Example:

            In [1]:    from seo_tools.generic import _http2

                       _http2('https://www.example.com')

            Out [1]:   True

        Attributes:

            url (str): A url whose HTTP/2 support status is to be determined

        Returns:

            Supports HTTP/2? (boolean):
                A boolean of if the domain is supported or not.

                True, if supported
                False, if not supported
    '''
    url = clean_url(url)
    c = HTTP20Connection(url)
    try:
        c.request('GET', '/')
        return True
    except AssertionError:
        return False

async def _https(url):
    '''
        Determines if a given url supports HTTPS protocol

        Ths function serves as the function run by the shell within the
            '__init__.py' file of this module. To run multiple tests concurrently,
            send a list of urls to the 'https' function found there.

        Example:

            In [1]:    from seo_tools.generic import _https

                       _https('https://www.example.com')

            Out [1]:   True

        Attributes:

            url (str): A url whose HTTPS support status is to be determined

        Returns:

            Supports HTTPS? (boolean):
                A boolean of if the domain is supported or not.

                True, if supported
                False, if not supported
    '''
    session = aiohttp.ClientSession()
    url = 'http://' + clean_url(url)
    async with session.request('GET', url=url) as resp:
        u = await resp.url
        return ('https://' in resp.url)

async def _mobile_friendly(url):
    request_url = f'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?url={url}&key=key'
    resp = await post(request_url)
    return r['mobileFriendliness'] == 'MOBILE_FRIENDLY'

async def _pagespeed(url, strategy=None):
    if strategy is not None:
        request_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=performance&strategy={strategy}&key=key'
        data = await get(url=request_url_m)
        return int(data['lighthouseResult']['categories']['performance']['score'] * 100)
    else:
        request_url_m = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=performance&strategy=mobile&key=key'
        m_data = await get(url=request_url_m)
        mobile_ps = int(m_data['lighthouseResult']['categories']['performance']['score'] * 100)
        request_url_d = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=performance&strategy=desktop&key=key'
        d_data = await get(url=request_url_d)
        desktop_ps = int(d_data['lighthouseResult']['categories']['performance']['score'] * 100)
        return [mobile_ps, desktop_ps]

async def _lighthouse(url, strategy=None):
    if strategy is not None:
        request_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=accessibility&category=best-practices&category=performance&category=pwa&category=seo&strategy={strategy}&key=key'
        data = await get(url=request_url)
        return LighthouseReport(strategy, data)
    else:
        request_url_m = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=accessibility&category=best-practices&category=performance&category=pwa&category=seo&strategy=mobile&key=key'
        m_data = await get(url=request_url_m)

        request_url_d = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=accessibility&category=best-practices&category=performance&category=pwa&category=seo&strategy=desktop&key=key'
        d_data = await get(url=request_url_d)
        s = [LighthouseReport('mobile', m_data), LighthouseReport('desktop', d_data)]
        return s
