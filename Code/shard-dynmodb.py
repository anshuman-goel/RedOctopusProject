# script to read data from Kinesis, extract hashtags and store into
# dynamoDB

import boto3
import time
import json
import decimal

# aws creds are stored in ~/.boto

# Connent to the kinesis stream
kinesis = boto3.client("kinesis")
shard_id = 'shardId-000000000000'  # only one shard
shard_it = kinesis.get_shard_iterator(StreamName="twitter", ShardId=shard_id, ShardIteratorType="LATEST")["ShardIterator"]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Twitter')

while 1 == 1:
    out = kinesis.get_records(ShardIterator=shard_it, Limit=100)
    #print(out['Records'])
    for record in out['Records']:
        tweet_record = json.loads(record['Data'].decode('utf-8'))
        # print(record['Data'])
        if 'id_str' in tweet_record.keys() and 'lang' in tweet_record.keys() \
        and 'text' in tweet_record.keys() and 'source' in tweet_record.keys():
            if 'user' in tweet_record.keys() and tweet_record['id_str'] is not None\
            and tweet_record['lang'] is not None and tweet_record['text'] is not None\
            and tweet_record['source'] is not None:
                tweet_user = tweet_record['user']
                """
                    id, friends_count, statuses_count, favourites_count - int
                    rest all attributes are string
                """
                #print(tweet_user['time_zone'])
                if 'id' in tweet_user.keys() and 'name' in tweet_user.keys() \
                and 'time_zone' in tweet_user.keys() and 'friends_count' in tweet_user.keys() \
                and 'screen_name' in tweet_user.keys() and 'statuses_count' in tweet_user.keys() \
                and 'favourites_count' in tweet_user.keys() and 'description' in tweet_user.keys():
                    if tweet_user['id'] is not None and tweet_user['name'] is not None \
                    and tweet_user['time_zone'] is not None and tweet_user['friends_count'] is not None \
                    and tweet_user['screen_name'] is not None and tweet_user['statuses_count'] is not None \
                    and tweet_user['favourites_count'] is not None and tweet_user['description'] is not None:
                        if 'place' in tweet_record.keys():
                            tweet_place = tweet_record['place']
                            if 'country' in tweet_place.keys() and 'country_code' in tweet_place.keys() \
                            and 'full_name' in tweet_place.keys() and 'place_type' in tweet_place.keys():
                                #print(tweet_place['country'] .encode('utf8'))
                                if tweet_place['country'] is not None and tweet_place['country_code'] is not None \
                                and tweet_place['full_name'] is not None and tweet_place['place_type'] is not None:
                                    print(tweet_place['place_type'] .encode('utf8'))
    # Refer http://boto3.readthedocs.io/en/latest/guide/dynamodb.html for pushing data in DynamoDB
    """tweet_text=record['Data'].encode('unicode_escape')#decode('utf-8')
        #print(tweet_text)
        if 'text' in json.loads(tweet_text):
            text = json.loads(tweet_text)['text']
            print(text)
        if 'entities' in json.loads(tweet_text):
            htags = json.loads(tweet_text)['entities']['hashtags']
            if htags:
                for ht in htags:
                    htag = ht['text']
                    checkItemExists = table.get_item(Key={'hashtag':htag})
                    if 'Item' in checkItemExists:
                        response = table.update_item(Key={'hashtag': htag},
							UpdateExpression="set htCount  = htCount + :val",
							ConditionExpression="attribute_exists(hashtag)",
							ExpressionAttributeValues={
								':val': decimal.Decimal(1)
							},
							ReturnValues="UPDATED_NEW"
						)
                    else:
                                		response = table.update_item(
                                        		Key={
                                                		'hashtag': htag
                                        		},
                                        		UpdateExpression="set htCount = :val",
                                        		ExpressionAttributeValues={
                                                		':val': decimal.Decimal(1)
                                        		},
                                        		ReturnValues="UPDATED_NEW"
                                		)"""
    shard_it = out["NextShardIterator"]
    time.sleep(1.0)
