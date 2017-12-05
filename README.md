# RedOctopusProject

How to proceed:
1. Install all the requirements.
    Boto3
    Twitter API
    HTTP
    Twitter
    awscli
  These can be installed using setup script. The setup script also makes sure to install python and pip and sets up the environment       parameters
2. Update your AWS credentials using aws configure command. Use same AWS credentials on all the machines chosen to move the data to the same DynamoDB location. This can be done by entering “aws configure” command in terminal of the machine and updating the required fields.
3. Create Twitter API. One access key can be used used for for two simultaneously connections. Store the Twitter credentials in the “twitterCreds.py” file
4. To create Kinesis stream run “create-stream.py”. 
5. Run Twitter Kinesis to generate data through command line
    python twitter-kinesis.py <num_threads> <shard_id>
6. If table doesn’t exists in DynamoDB create the table by running “create-dynamodb.py”.
7. To start reading data from Kinesis and storing them persistently by running “shard-dynmodb.py”.
8. Create EMR Cluster as per the need.
9. Transfer data from DynamoDB to hadoop in EMR shell by running
      hive -f fetch_data.hql
10. To run the sample analysis again run it using
      hive -f hive.hql


