import os
import time
import urllib2

import argparse
import json
import oauth2


parser = argparse.ArgumentParser(description='Fetch tweets')
parser.add_argument('--max_tweets', action="store", dest="max_tweets",
                    type=int, default=0)
parser.add_argument('--location', action="store", dest="location",
                    default=None)
parser.add_argument('--download_time', action="store", dest="download_time",
                    default=0)

access_token_key = os.environ['ACCESS_TOKEN_KEY']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']


class TwitterStream():
    def __init__(self, location=None):
        url = get_url(location)
        _debug = 0
        oauth2_token = oauth2.Token(key=access_token_key,
                                  secret=access_token_secret)
        oauth2_consumer = oauth2.Consumer(key=consumer_key,
                                        secret=consumer_secret)
        signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()
        http_handler = urllib2.HTTPHandler(debuglevel=_debug)
        https_handler = urllib2.HTTPSHandler(debuglevel=_debug)
        req = oauth2.Request.from_consumer_and_token(oauth2_consumer,
                                                    token=oauth2_token,
                                                    http_method="GET",
                                                    http_url=url,
                                                    parameters=[])
        req.sign_request(signature_method_hmac_sha1, oauth2_consumer,
                         oauth2_token)
        self.url = req.to_url()
        self.opener = urllib2.OpenerDirector()
        self.opener.add_handler(http_handler)
        self.opener.add_handler(https_handler)

    def __enter__(self):
        return self.opener.open(self.url, None)

    def __exit__(self, *_):
        try:
            self.opener.close()
        except:
            pass
        return True

def get_url(location):
    if location:
        return "https://stream.twitter.com/1.1/statuses/filter.json" \
                "?locations=%s" % location
    return "https://stream.twitter.com/1.1/statuses/sample.json"


def fetch_samples(location, max_tweets, download_time, output=None):
    count = 0
    start_at = time.time()
    def limit_reached():
        execution_seconds = int(time.time() - start_at)
        return (max_tweets and (count > int(max_tweets))) \
                or (download_time and (execution_seconds > int(download_time)))

    with TwitterStream(location) as response:
        for line in response:
            if 'delete' in json.loads(line):
                continue
            output.write(line + '\n')
            count = count + 1
            if limit_reached():
                break
    return True

if __name__ == '__main__':
    args = parser.parse_args()
    fetch_samples(args.location, args.max_tweets, args.download_time)
