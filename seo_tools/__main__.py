import sys

from datetime import datetime
from seo_tools import lighthouse

fname = "pyblighthouse_{}.csv".format(str(datetime.now())[:11])

def blighthouse(urlLs=None):
    f = open(sys.argv[1], 'r').read()
    urlLs = [site for site in f.split('\n') if site != '']
    lh = lighthouse(urlLs)
    print('Writing Reports')
    c = list(lh[0].desktop.categories.keys())
    a = list(lh[0].mobile.audits.keys())
    h = ['URL', 'Device'] + c + a
    f = open(fname, 'w+')
    f.write(",".join(h) + "\n")
    for l in lh:
        r = l.to_csv(c, a, f)
    f.close()
    return lh
