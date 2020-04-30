import os
import json
import seo_tools


modulepath = os.path.abspath(os.path.join(seo_tools.__file__, os.pardir))

class Auth:

    def __init__(self, tup):
        self.id = tup[0]
        self.key = tup[1]

class Credentials:

    google = Auth((None, 'key'))
    gt_metrix = Auth(('email', 'key'))
    moz = Auth(('account', 'key'))


class APIs:

    lh_cats = ['accessibility', 'best-practices', 'performance', 'pwa', 'seo']
    lh_all = 'category=accessibility&category=best-practices&category=performance&category=pwa&category=seo'
    mf_api = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?url=%s&key=%s'
    lh_api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&%s&strategy=%s&key=%s'
    gtm_start = 'https://gtmetrix.com/api/0.1/test'
    gtm_fetch = 'https://gtmetrix.com/api/0.1/test/%s'
    moz_api = 'http://lsapi.seomoz.com/linkscape/url-metrics/%s?%s'
    moz_batch_api = 'http://lsapi.seomoz.com/linkscape/url-metrics/?%s'


    lh_api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&category=performance&strategy=mobile&key=%s'
