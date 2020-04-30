

class LighthouseReport:
    ''' The Lighthouse report class. Used to parse results of an audit '''

    def __init__(self, strategy, r=None):
        self.strategy = strategy
        if r is not None:
            self._parse(r)

    def _parse(self, resp):
        self.categories = {}
        for key, value in resp['lighthouseResult']['categories'].items():
            self.categories[key] = value
        self.audits = {}
        for key, value in resp['lighthouseResult']['audits'].items():
            self.audits[key] = value

    def _to_csv(self, u,  f):
        s = open(f, 'w+')
        st = f'{u}'
            
