## Example to use twitter api and feed data into kinesis

from TwitterAPI import TwitterAPI
import boto3
import json
import twitterCreds


import threading
import time

class StreamTwitterData (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        self.count = 0
        self.tweets = []
        self.api = api
        self.kinesis = kinesis
    def run(self):
        while (1):
            r = self.api.request('statuses/filter', {'locations':'-180,-90,180,90'})
            self.tweets = []
            self.count = 0
            for item in r:
                jsonItem = json.dumps(item)
                self.tweets.append({'Data':jsonItem, 'PartitionKey':"filler"})
                self.count += 1
                if self.count == 100:
                    self.kinesis.put_records(StreamName="twitter", Records=self.tweets)
                    self.count = 0
                    self.tweets = []

## twitter credentials

consumer_key = twitterCreds.consumer_key
consumer_secret = twitterCreds.consumer_secret
access_token_key = twitterCreds.access_token_key
access_token_secret = twitterCreds.access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

kinesis = boto3.client('kinesis')

thread1 = StreamTwitterData(api, kinesis)
thread2 = StreamTwitterData(api, kinesis)
#thread3 = StreamTwitterData(api, kinesis)
#thread4 = StreamTwitterData(api, kinesis)

thread1.start()
thread2.start()
#thread3.start()
#thread4.start()

thread1.join()
thread2.join()
#thread3.join()
#thread4.join()
