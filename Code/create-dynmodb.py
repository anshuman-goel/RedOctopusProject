
## create a table to store twitter hashtags in DynamoDB
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='Twitter',
    KeySchema=[
        {
            'AttributeName': 'id_str',
            'KeyType': 'HASH',
        },
        {
            'AttributeName': 'id',
            'KeyType': 'RANGE',
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id_str',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'id',
            'AttributeType': 'S',
        },
    ],
    # pricing determined by ProvisionedThroughput
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='Twitter')
