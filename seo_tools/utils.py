import aiohttp
import asyncio
import inspect
import logging
import re
import time


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}


async def get(url, count=0, **kwargs,):
    if 'session' in kwargs:
        session = kwargs.get('session')
        del kwargs['session']
        return await _send_get_request(session=session, url=url, **kwargs)
    else:
        async with aiohttp.ClientSession() as session:
            return await _send_get_request(session=session, url=url, **kwargs)


async def post(url, count=0, **kwargs,):
    if 'session' in kwargs:
        session = kwargs.get('session')
        del kwargs['session']
        return await _send_post_request(session=session, url=url, **kwargs)
    else:
        async with aiohttp.ClientSession() as session:
            return await _send_post_request(session, url, count=count+1, **kwargs)


async def _send_get_request(session, url, count=0, **kwargs):
    '''
        Sends a standard get request to a url, passing the keyword arguments

        If returned a non-200 status code 3 times, returns an error message


        Args:
            url (str): the url to be called by the get request.

        Kwargs:
            count (int): The recursion count, function will exit after three
                attempts

            **kwargs (any): additional arguments for the passing of the request

        Returns:

            A tuple of a boolean for success and a reponse message or a error
                message
    '''
    try:
        resp = await session.request('GET', url=url, **kwargs)
    except:
        if count == 2:
            return None
        return await _send_get_request(session, url, count=count+1, **kwargs)
    return await resp.json()


async def _send_post_request(session, url, count=0, **kwargs):
    '''
        Sends a standard post request to a url, passing the keyword arguments

        If returned a non-200 status code 6 times, returns an error message


        Args:
            url (str): the url to be called by the get request.

        Kwargs:
            count (int): The recursion count, function will exit after three
                attempts

            **kwargs (any): additional arguments for the passing of the request

        Returns:

            A tuple of a boolean for success and a reponse message or a error
                message
    '''
    try:
        resp = await session.request('POST', url=url, **kwargs)
    except:
        if count == 2:
            return None
        return await _send_post_request(session, url, count=count+1, **kwargs)

    return await resp.json()


def clean_url(url):
    '''
        Removes the protocol from a given url and formats it for certain
            tools.
    '''
    return re.sub(r'(^\w+:|^)\/\/', "", url).replace('www.', '')


async def batch(func, urls, **kwargs):
    tasks = []
    for url in urls:
        tasks.append(func(url, **kwargs))
    return await asyncio.gather(*tasks, return_exceptions=True)
