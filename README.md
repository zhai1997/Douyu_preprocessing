# Douyu_preprocessing
This document describes the pre-processing of large data in the Douyu project with limited resources. In order to finish this task, we had to drop data that are irrelevant with our research goal and break down the task into several steps. So, it is necessary to keep down the considerations when we decided to drop data and the relationship among the steps, so that we can double check the codes in case we have find something strange and it is useful if someone wants to join later and wonders what we have done.

### Whole picture
The original data are Msg (bullet chat), Streamer (information about the influencer), Star_live (information about one live), and Follower (the number of followers for each influencer). They are all in txt format. The main challenges are:

- Msg and Start_live are over 100GB, which causes a lot of trouble for the processing
- Msg contains a lot of dirty records

Our methods to solve the problems above are:

1. Imported two small data sets Follower and Streamer into MySQL database.
2. Joined the two small tables.
3. Analyzed the distributions of data we got in Step 2 to determine the data of interest.
4. Filtered the data with Python in advance, we only kept data of interest. In this step we detected dirty records, deleted them and kept down the information of the row we deleted.
5. Further broke down the big table into several small views and joined each small view with the table we got in Step 2.
6. Used Google API to calculate the sentiment and joined the results with the table in Step 5.

### Imported and joined two small data sets
These two steps are easy. 
- Walked through the directories with Python to generate SQL commands, and ran the SQL commands. [Codes](small_datasets/import_data.py)
- Created tables in MySQL. [Codes](small_datasets/create_table.sql)
- Originally, Follower was a long table with records of different years in different rows. We changed the structure of it to make the records of one streamer in a single row. [Codes](small_datasets/change_the_structure.sql)
- Then merged the tables. [Codes](small_datasets/join_features.sql)

### Determined the data of interest
- Explored the distribution of followers of streamers, blocked by the types of streamers. [star_type](distributions/task1.sql), [followers](distributions/task2.sql),  [percentile of followers](distributions/task31.sql), [percentile of followers by star_type](distributions/task32.sql), [check if the percentile is right](distributions/check.sql)
- Selected two types of streamers, in order to compare the top and middle level streamers.
- Decided to only consider the lives between 2020-12-11 and 2020-12-14.

### Filtered big data sets
- Msg: The mistakes of data are various, and it is impossible to exhaust them, so we had to let the Exceptions happen, and used Python to capture the Exception. Then we dealt only with the manageable Exceptions while dropping and taking down the other Exceptions. [Codes](filter/top_mid.py)
- Start_live: Filtered Start_live data in a similar manner. [Codes](filter/to_csv_start_live.py)
- Imported the filtered data into MySQL database. [Codes](filter/import_csv.py)

### Further broke down the data sets and joined tables
- Further broke down the still big tables to several small views and joined the views with the merged two small tables. Note that we filtered out data without start_live records. [Codes](broke_joined/join_table_5day.sql)
- Wrote the results into csv file.

### Cleaned data and joined sentiment
- Cleaned the data and excluded data with unrealistic end time of live. [Codes](sentiment/sentiment.py)
- Grouped the data every 10 minutes and joined the bullet chat messages in the window of ten minutes to one row.
- Used Google API to calculate the sentiment and joined the sentiment to get the subsample.
