from TwitterAPI import TwitterAPI
import boto3, json
import twitterCreds
import threading, time
from threading import Thread
import sys, urllib3, http

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
        print("Producer started...")
        while (1):
            try:
                r = self.api.request('statuses/filter', {'locations':'-180,-90,180,90'})
                self.tweets = []
                self.count = 0
                for item in r:
                    jsonItem = json.dumps(item)
                    #self.tweets.append({'Data':jsonItem, 'PartitionKey':"filler"})
                    tweet_buffer.append({'Data':jsonItem, 'PartitionKey':"filler"})
                    self.count += 1
                    # place the data into a global buffer shared among producer and all consumers
                    if len(tweet_buffer) >= MAX_BUFF_LEN:
                        del tweet_buffer[0]
            except (urllib3.exceptions.ProtocolError, http.client.IncompleteRead) as e:
                continue


class TwitterDataConsumer (threading.Thread):
    def __init__(self, api, kinesis):
        threading.Thread.__init__(self)
        self.tweet_record = []
        self.api = api
        self.kinesis = kinesis

    def run(self):
        global tweet_buffer
        tweet_record = []
        print("Consumer started...")

        while (1):
            # check if the buffer has atleast one tweet to read
            if len(tweet_buffer) != 0:
                tweet_record = []
                # read the tweet and remove from the buffer
                tweet_record.append(tweet_buffer[0])
                #del tweet_buffer[0]
                # push the tweet into aws kinesis
                #print "consumer reading data from buffer and pushing into kinesis..."
                self.kinesis.put_records(StreamName="twitter", Records=tweet_record)
                # del tweet_record[0]




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
    if len(sys.argv) > 1:
        num_consumers = int(sys.argv[1])
    else:
        num_consumers = 10
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
