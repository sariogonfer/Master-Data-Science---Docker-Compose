from datetime import datetime
import os

from pymongo import MongoClient

from twitter_stream import fetch_samples
from twitter_feeling import MyJob

def main():
    access_token_key = os.getenv('ACCESS_TOKEN_KEY')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    if not access_token_key or not access_token_secret:
        return False

    mongodb_host = os.getenv('MONGODB_HOST')
    mongodb_port = int(os.getenv('MONGODB_PORT'))
    mongodb_db = os.getenv('MONGODB_DB')
    location_filter = os.getenv('LOCATION_FILTER')
    max_tweets = os.getenv('MAX_TWEETS', 100)
    download_time = os.getenv('DOWNLOAD_TIME', 60)
    ts_str = datetime.now().strftime('%Y%m%d_%H%M_%s')
    with open('/tmp/%s' % ts_str, 'w') as file_:
        fetch_samples(location_filter, max_tweets, download_time, file_)
        my_job = MyJob(args=[file_.name, '-r', 'emr', '--archive',
                             './code/pickles.tar.gz#pickles', '--no-output',
                             '-c', './mrjob.conf'])
        with my_job.make_runner() as runner:
            runner.run()
            db_ = MongoClient(mongodb_host, mongodb_port)[mongodb_db]
            collection = db_['feelings_' + ts_str]
            for key, value in my_job.parse_output(runner.cat_output()):
                post = {'label': key[0], 'value': key[1], 'count': value[0],
                        'score': value[1]}
                collection.insert_one(post)
                print key, value

if __name__ == '__main__':
    main()
