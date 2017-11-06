#emr

# first  add this to  bashrc fiel and change the source export PATH="$PATH:$HIVE_HOME/bin"

#create an external table for the data in dynamodb which has to be mapped to the hive to copy data form dynamodb to hdfs
#CREATE EXTERNAL TABLE twitter_dynamodb(hash string, count bigint) STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' TBLPROPERTIES ("dynamodb.table.name" = "hashtags", "dynamodb.column.mapping" = "hash:hashtag,count:htCount");

#create a table in hdfs where the data has to be copied.
#create external table hdfs_twitter (hash string, coutn bigint) STORED AS SEQUENCEFILE location 'hdfs://rachittwittertest/'
#do add the way we want the data ot be stored in the file

#copy data from dynamodb to hdfs
#INSERT OVERWRITE TABLE hdfs_twitte_1r SELECT * from twitter_dynamodb;

import sys
from random import random
from operator import add

from pyspark import SparkContext


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    sc = SparkContext(appName="PythonPi")
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        print"#####################################################"
        #print _
        return _

    # count = sc.parallelize(xrange(1, n + 1), partitions).map(f).reduce(add)
    #print "Pi is roughly %f" % (4.0 * count / n)
    rdd_name = sc.textFile('hdfs:///user/hadoop/hive-test/000000_0').map(f).collect()
=======
    rdd_name = sc.textFile('hdfs://rachittwittertest/000000_0').map(f).collect()
>>>>>>> Update emr.py
    print rdd_name
    sc.stop()
