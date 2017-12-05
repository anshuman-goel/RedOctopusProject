 # RedOctopusProject

How to proceed:
1. Clone this git repository in all the machines which will be used for analysis.  
```git clone https://github.ncsu.edu/CSC591-DIC/RedOctopusProject```  
2. Install all the requirements.  
   * Boto3  
   * Twitter API  
   * HTTP  
   * Twitter  
   * awscli  

These can be installed using setup script. The setup script also makes sure to install python and pip and sets up the environment       parameters.  
3. Update your AWS credentials using aws configure command. Use same AWS credentials on all the machines chosen to move the data to the same DynamoDB location. This can be done by entering “aws configure” command in terminal of the machine and updating the required fields.  
4. Create Twitter API. One access key can be used used for for two simultaneously connections. Store the Twitter credentials in the “twitterCreds.py” file.  
5. To create Kinesis stream run “create-stream.py”.  
6. Run Twitter Kinesis to generate data through command line  
    ```python twitter-kinesis.py <num_threads> <shard_id>```  
7. If table doesn’t exists in DynamoDB create the table by running “create-dynamodb.py”.  
8. To start reading data from Kinesis and storing them persistently by running “shard-dynmodb.py”.  
9. Create EMR Cluster as per the need.  
10. Transfer data from DynamoDB to hadoop in EMR shell by running  
      ```hive -f fetch_data.hql```
11. To run the sample analysis again run it using  
      ```hive -f hive.hql```


