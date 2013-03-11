import urllib2
import oauth2 as oauth
import os

class EConfigFileNotFound(Exception):
    def __init__(self, message="Config file not found"):
        self.message = message
    def __str__(self, message):
        return message

class EConfigParameterNotFound(Exception):
    def __init__(self, message="Config parameter not found"):
        self.message = message
    def __str__(self, message):
        return message

class Twitter:
    def __init__(self, handle):
        self._handle = handle
        self._http_method = 'POST'
        self._url = 'https://api.twitter.com/1/statuses/update.json'
        self.configure(handle)
    def configure(self, handle): 
        self._config_file = '%s/.%s' % (os.environ['HOME'], handle)
        if not os.path.exists(self._config_file):
            raise EConfigFileNotFound
        config = {}
        with open(self._config_file) as cfile:
            for line in cfile:
                if not line.startswith("#"):
                    (key, val) = line.split(':')
                    config[str(key.strip())] = str(val.strip().strip('\n'))
        #print "Twitter: configure: config: %s" % config
        if 'access_token_key' not in config:
            raise EConfigParameterNotFound('access_token_key is missing')
        if 'access_token_secret' not in config:
            raise EConfigParameterNotFound('access_token_secret is missing')
        if 'consumer_key' not in config:
            raise EConfigParameterNotFound('consumer_key is missing')
        if 'consumer_secret' not in config:
            raise EConfigParameterNotFound('consumer_secret is missing')
        self._access_token_key    = config['access_token_key']
        self._access_token_secret = config['access_token_secret']
        self._consumer_key        = config['consumer_key']
        self._consumer_secret     = config['consumer_secret']
        self._oauth_token    = oauth.Token(key=self._access_token_key, secret=self._access_token_secret)
        self._oauth_consumer = oauth.Consumer(key=self._consumer_key, secret=self._consumer_secret)

    def _request(self, status):
        parameters = {'status': status}
        request = oauth.Request.from_consumer_and_token(self._oauth_consumer, 
                                                    token=self._oauth_token, 
                                                    http_method=self._http_method, 
                                                    http_url=self._url, 
                                                    parameters=parameters)
        request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), 
                         self._oauth_consumer, self._oauth_token)
        return request

    def _get_header(self, request):
        return request.to_header()

    def _get_postdata(seld, request):
        return request.to_postdata()

    def tweet(self, status):
        t_request = self._request(status)
        t_postdata = self._get_postdata(t_request)
    
        t_opener = urllib2.OpenerDirector()
        t_opener.add_handler(urllib2.HTTPSHandler())

        response = t_opener.open(self._url, t_postdata)
        t_opener.close()

if __name__ == '__main__':
    t = Twitter('HadoopSO')
    t.tweet("this is a sample tweet message!!")

