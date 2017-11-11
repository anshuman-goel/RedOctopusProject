CREATE EXTERNAL TABLE twitter_dynamodb(name string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name" = "Twitter", "dynamodb.column.mapping" = "name:name");

create external table twitter_hdfs (name string) STORED AS SEQUENCEFILE location 'hdfs:///twitter/';

INSERT OVERWRITE TABLE twitter_hdfs SELECT * from twitter_dynamodb;
