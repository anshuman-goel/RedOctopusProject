## Example to use twitter api and feed data into kinesis

from TwitterAPI import TwitterAPI
import boto3
import json
import twitterCreds


import threading
import time
from threading import Thread
import sys


MAX_BUFF_LEN = 15000
tweet_buffer = []

class TwitterDataProducer (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        self.count = 0
        self.tweets = []
        self.api = api
        self.kinesis = kinesis
    def run(self):
        global tweet_buffer
        print "Producer started..."
        while (1):
            r = self.api.request('statuses/filter', {'locations':'-180,-90,180,90'})
            self.tweets = []
            self.count = 0
            for item in r:
                jsonItem = json.dumps(item)
                #self.tweets.append({'Data':jsonItem, 'PartitionKey':"filler"})
                tweet_buffer.append({'Data':jsonItem, 'PartitionKey':"filler"})
                self.count += 1
                # place the data into a global buffer shared among producer and all consumers
                #mutex.acquire()
                if len(tweet_buffer) >= MAX_BUFF_LEN:
                    del tweet_buffer[0]
                    print "producer: deleting entry..."


                #mutex.release()


class TwitterDataConsumer (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        self.tweet_record = []
        self.api = api
        self.kinesis = kinesis
    def run(self):
        global tweet_buffer
        tweet_record = []
        print "Consumer started..."
        cnt = 0
        size = 0
        while (1):
            # check if the buffer has atleast one tweet to read
            #mutex.acquire()
            if len(tweet_buffer) != 0:
                
                # read the tweet and remove from the buffer
                tweet_record.append(tweet_buffer[0])
                #del tweet_buffer[0]
                # push the tweet into aws kinesis
                #print "consumer reading data from buffer and pushing into kinesis..."
                self.kinesis.put_records(StreamName="twitter", Records=tweet_record)
                cnt += 1
                size += sys.getsizeof(tweet_record)
                if cnt == 1500:
                    print size
                    cnt = 0
                del tweet_record[0]
            #mutex.release()




def main():

    ## twitter credentials

    consumer_key = twitterCreds.consumer_key
    consumer_secret = twitterCreds.consumer_secret
    access_token_key = twitterCreds.access_token_key
    access_token_secret = twitterCreds.access_token_secret

    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    kinesis = boto3.client('kinesis')

    producer = TwitterDataProducer(api, kinesis)
    producer.start()
    num_consumers = int(sys.argv[1])
    for i in range(num_consumers):
        consumer = TwitterDataConsumer(api, kinesis)
        consumer.start()


#thread2 = StreamTwitterData(api, kinesis)
    #thread3 = StreamTwitterData(api, kinesis)
    #thread4 = StreamTwitterData(api, kinesis)

#thread1.start()
#thread2.start()
    #thread3.start()
    #thread4.start()

#thread1.join()
#thread2.join()
    #thread3.join()
    #thread4.join()


if __name__ == "__main__":
    main()
