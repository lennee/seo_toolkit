import asyncio
import aiohttp

import logging

from seo_tools.utils import post
from seo_tools.config import Credentials


async def mf_single(url):
    request_url = f'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?url={url}&key=%s'
    resp = await post(request_url % Credentials.google.key)
    return r['mobileFriendliness'] == 'MOBILE_FRIENDLY'
