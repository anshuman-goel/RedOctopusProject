# RedOctopusProject

How to proceed:
1. Install all the requirements.
2. Update your AWS credentials using aws configure command.
3. Run Create Kinesis.
4.Run the setuo script like ./setup to setup the server by installing the aws cli and the reqiured python packages for the twitter Kinesis code to run.
5.Configure the aws cli by typing aws configure and updating the required fields.
6. Run Twitter Kinesis. like python twitter-kinesis.py <num_threads> <shard_id> 
7. Run create DynamoDB.
8. Run DynamoDB program.
9. Transfer data to hadoop
10. Run spark program
