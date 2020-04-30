import asyncio
import aiohttp

import time
import hmac
import base64
from hashlib import sha1
from urllib.parse import urlencode, quote

from seo_tools.config import Credentials
from seo_tools.utils import get, post

c = Credentials

def generate_moz_credentials(cols=103079215104):
    ''' Generate the necessary credentials for MozScapes API calls '''

    expires = str(int(time.time() + 300))
    return urlencode({
        "Cols": cols,
        "Limit": 4,
        "AccessID": c.moz.id,
        "Expires": expires,
        "Signature": base64.b64encode(hmac.new(c.moz.key.encode('utf-8'), (c.moz.id + '\n' + expires).encode('utf-8'), sha1).digest())
    })

async def moz_single(url, cols=103079215104):
    request_url = f'http://lsapi.seomoz.com/linkscape/url-metrics/{quote(url)}?{generate_moz_credentials(cols)}'
    async with aiohttp.ClientSession() as session:
        r = await get(session=session, url=request_url)
    return [r['pda'], r['upa']]

async def moz_batch(url_list, cols=103079215104):
    request_url = f'http://lsapi.seomoz.com/linkscape/url-metrics/?{generate_moz_credentials(cols)}'
    async with aiohttp.ClientSession() as session:
        data = await post(session=session, url=request_url, json=url_list)
    return [(r['pda'], r['upa']) for r in data]
