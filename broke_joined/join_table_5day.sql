SET global max_heap_table_size=53687091200000; 
SET global tmp_table_size=53687091200000;
SET GLOBAL innodb_buffer_pool_size=6710886400000;
USE douyu;

select 
case when start_time is not null then
MD5(concat(FROM_UNIXTIME(start_time),b.room_id))
else null end as live_id,
b.room_id,
user_id,
content,
if_fan,
if_vip,
FROM_UNIXTIME(b.time) as time,
startype_1,
startype_2,
startype_3,
gender,
age,
community_id,
sign_date,
location_1,
location_2,
FROM_UNIXTIME(start_time) as start_time,
FROM_UNIXTIME(end_time) as end_time,
follower_num_2017,
follower_num_2018,
follower_num_2019
from ( 
SELECT 
user_id,
room_id, 
content, 
if_fan, 
UNIX_TIMESTAMP(time) as time,
if_vip
FROM dt_top_2019
where substr(time,1,10) in ('2019-12-11')
) as b
LEFT JOIN (
	SELECT
		room_id,
		startype_1,
		startype_2,
		startype_3,
		gender,
		age,
		community_id,
		sign_date,
		location_1,
		location_2 
	FROM
		feature_table
	) st ON b.room_id = st.room_id
inner JOIN ( 
	SELECT DISTINCT room_id, start_time, end_time FROM start_live_only2019
	where substr(FROM_UNIXTIME(start_time),1,10) in ('2019-12-10','2019-12-11','2019-12-12')
	) slt 
	ON (b.room_id = slt.room_id 
	AND b.time >= slt.start_time 
	AND b.time <= slt.end_time)
inner join(
	select 
	*
	from
	follower_wide
)follower_t
on b.room_id=follower_t.room_id
where follower_num_2019 is not null
and start_time is not null

into outfile 'F:\\Reasearch_PHBS\\Subsample\\20191211.csv'