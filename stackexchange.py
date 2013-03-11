import urllib2, tinyurl, StringIO, gzip
import simplejson as json

class StackExchange:
    def __init__(self, base_url='http://api.stackexchange.com/2.1', 
                 page=1, pagesize=10, order='asc', sort='creation', 
                 tagged='c', site='stackoverflow', qfilter='!6X9exmvAIMz.b'):
        self._base_url = base_url
        self._page = page
        self._pagesize = pagesize
        self._order = order
        self._sort = sort
        self._tagged = tagged
        self._site = site
        self._filter = qfilter

    def _request(self, url):
        request = urllib2.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        req_open = urllib2.build_opener()
        conn = req_open.open(request)
        req_data = conn.read()

        # Handle compressed responses.
        # (Stack Exchange's API sends its responses compressed but intermediary
        # proxies may send them to us decompressed.)
        if conn.info().getheader('Content-Encoding') == 'gzip':
            data_stream = StringIO.StringIO(req_data)
            gzip_stream = gzip.GzipFile(fileobj=data_stream)
            actual_data = gzip_stream.read()
        else:
            actual_data = req_data
        conn.close()
        return json.loads(actual_data)['items']

    def _to_tinyurl(self, result):
        for item in result:
            item['link'] = tinyurl.create_one(item['link'])
        return result

    def _get_url(self, url, **kwargs):
        url += 'page=%d&'     % self._page     if 'page'     not in kwargs else 'page=%d&'     % kwargs['page']
        url += 'pagesize=%d&' % self._pagesize if 'pagesize' not in kwargs else 'pagesize=%d&' % kwargs['pagesize']
        if 'fromdate' in kwargs: url += 'fromdate=%d&' % kwargs['fromdate']
        if 'todate'   in kwargs: url += 'todate=%d&'   % kwargs['todate']
        url += 'order=%s&'    % self._order  if 'order'  not in kwargs else 'order=%s&'  % kwargs['order']
        if 'minval' in kwargs: url += 'min=%d&' % kwargs['minval']
        if 'maxval' in kwargs: url += 'max=%d&' % kwargs['maxval']
        url += 'sort=%s&'     % self._sort   if 'sort'   not in kwargs else 'sort=%s&'   % kwargs['sort']
        url += 'tagged=%s&'   % self._tagged if 'tagged' not in kwargs else 'tagged=%s&' % kwargs['tagged']
        url += 'site=%s&'     % self._site   if 'site'   not in kwargs else 'site=%s&'   % kwargs['site']
        url += 'filter=%s'    % self._filter if 'filter' not in kwargs else 'filter=%s'  % kwargs['filter']
        #print "StackExchange: _get_url: url: %s" % url 
        return url

    def get_unanswered_questions(self, **kwargs):
        url = self._base_url + '/questions/unanswered?'
        result = self._request(self._get_url(url, **kwargs))
        return self._to_tinyurl(result)
        
    def get_noanswered_questions(self, **kwargs):
        url = self._base_url + '/questions/no-answers?'
        result = self._request(self._get_url(url, **kwargs))
        return self._to_tinyurl(result)
        
    def get_featured_questions(self, **kwargs):
        url = self._base_url + '/questions/featured?'
        result = self._request(self._get_url(url, **kwargs))
        return self._to_tinyurl(result)

if __name__ == '__main__':
    se = StackExchange()
    print se.get_unanswered_questions(pagesize=10, site='stackoverflow', tagged='javascript', fromdate=1362096000, todate=1362873600)
#    print se.get_noanswered_questions(page=2, fromdate=1362096000, todate=1362873600)
#    print se.get_unanswered_questions()
#    print se.get_noanswered_questions()
    
