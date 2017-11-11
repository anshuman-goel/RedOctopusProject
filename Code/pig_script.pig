input_lines = LOAD 'hdfs:///twitter/000000_0' using PIGStorage(,) AS (name:chararray);
 
 -- Extract words from each line and put them into a pig bag
 -- datatype, then flatten the bag to get one word on each row
 names = FOREACH input_lines GENERATE LOWER(line)) AS name;
 
 -- filter out any words that are just white spaces
 filtered_names = FILTER names BY name MATCHES '\\w+';
 
 -- create a group for each word
 name_groups = GROUP filtered_names BY name;
 
 -- count the entries in each group
 name_count = FOREACH name_groups GENERATE COUNT(filtered_names) AS count, group AS name;
 
 -- order the records by count
 ordered_name_count = ORDER name_count BY count DESC;
 STORE ordered_name_count INTO 'hdfs:///twitter/result/name_count.txt';
