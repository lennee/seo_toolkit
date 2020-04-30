import logging
import time

from seo_tools.config import Credentials, APIs
from seo_tools.utils import get, post

c = Credentials


class GTMetrix:

    def __init__(self, url):
        self.url = url
        self.test()

    def test(self):
        logging.info('Starting GT Metrix Test: {}\n'.format(self.url))
        r = self.start()
        if r[0]:
            return self.fetch((c.gt_metrix.id, c.gt_metrix.key))
        else:
            return r[1]

    def start(self):
        r = post(APIs.gtm_start, data={'url':self.url}, auth=(c.gt_metrix.id, c.gt_metrix.key))
        if r[0]:
            self.test_id = r[1]['test_id']
            self.poll_state_url = r[1]['poll_state_url']
        return r

    def fetch(self, auth):
        r = get(self.poll_state_url, auth=auth)
        if r[0]:
            if r[1]['state'] == 'completed':
                return self.parse(r[1])
            else:
                logging.info('GT Metrix Test Not Completed. Waiting and then trying again.')
                time.sleep(10)
                return self.fetch(auth)
        else:
            return r

    def parse(self, r):
        for key, val in r['results'].items():
            setattr(self, key, val)
        return self
