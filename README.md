# Douyu_preprocessing
This document describes the pre-processing of large data in the Douyu project with limited resources. In order to finish this task, we had to drop data that are irrelevant to our research goal and break down the task into several steps. So, it is necessary to keep down the considerations when we decided to drop data and the relationship between several steps, so that we can double check the codes when we have some new findings and it is useful if someone wants to join later and wonders what we have done.

### Whole picture
The original data are Msg (bullet chat), Streamer (information about the influencer), Star_live (information about one live), and Follower (the number of followers for each influencer). They are all in txt format. The main challenges are:
- Msg and Start_live are over 100GB, which causes a lot of trouble for the processing
- Msg contains a lot of dirty records

Our methods to solve the problems above are:
1. Imported two small data sets Follower and Streamer into MySQL database.
2. Joined the two small tables.
3. Analyzed data got in 2, and determined the data of interest.
4. Filtered the data with Python in advance, we only keep data of interest. In this step we detected dirty records, deleted them and kept down the information of the row we deleted.
5. Further broke down the big table into several small tables and join each small table with the table we got in 3.
6. Used Google API to calculate the sentiment and joined the results with the table in 5.


### Imported and joined two small data sets
These two steps are easy. 
- We just walked through the directories with Python to generate SQL commands, and ran the SQL commands.
- Created tables in MySQL.
- Originally, Follower was a long table with records of different years in different rows. We changed the structure of it to make the records of one streamer in the a single row.
- Then merged the tables.

### Determined the data of interest
- We explored the distribution of followers of streamers, blocked by the types of streamers.
- We selected two types of streamers, and we want to compare the top and middle level streamers.
- We decided to only consider the lives between 2020-12-11 and 2020-12-14.

### Filtered big data sets
- Msg: The mistakes of data are various, and we cannot exhaust them, so we had to make the Exceptions happen, and used Python to capture the Exception. Then we dealt only with the manageable Exceptions while dropping and keeping down other Exceptions.
- Start_live: Filtered Start_live data in a similar manner.
- Imported the filtered data into MySQL database.

### Further broke down the data sets and joined tables
- We further broke down the still big tables to several small views and joined the views with the merged two small tables. Note that we filtered out data without start_live records.
- Wrote the results into csv file.

### Cleaned data and joined sentiment
- We further cleaned the data and excluded data with unrealistic end time of live.
- Grouped the data every 10 minutes and joined the bullet chat messages in the window of ten minutes to one row.
- Used Google API to calculate the sentiment and joined the sentiment to get the subsample.
