SET SESSION max_heap_table_size=536870912000; 
SET SESSION tmp_table_size=536870912000; 
create table if not exists douyu.feature_table as
SELECT 
	COALESCE( st_t.room_id, fl_t.room_id ) AS room_id,
	startype_1,
	startype_2,
	startype_3,
	gender,
	age,
	community_id,
	sign_date,
	location_1,
	location_2,
	follower_num 
FROM
	(
	SELECT
		room_id,
		max( startype_1 ) AS startype_1,
		max( startype_2 ) AS startype_2,
		max(startype_3) as startype_3,
		max( gender ) AS gender,
		max( age ) AS age,
		max( community_id ) AS community_id,
		max(
		concat( date_1, ' ', date_2 )) AS sign_date,
		max( location_1 ) AS location_1,
		max( location_2 ) AS location_2 
	FROM
		douyu.streamer 
	GROUP BY
		room_id 
	) st_t
	left JOIN 
	( SELECT room_id, max(COALESCE(follower_num_2019,follower_num_2018,follower_num_2017)) AS follower_num FROM douyu.follower_wide group by room_id ) fl_t 
	ON st_t.room_id = fl_t.room_id
union 

SELECT 
	COALESCE( st_t.room_id, fl_t.room_id ) AS room_id,
	startype_1,
	startype_2,
	startype_3,
	gender,
	age,
	community_id,
	sign_date,
	location_1,
	location_2,
	follower_num 
FROM
	(
	SELECT
		room_id,
		max( startype_1 ) AS startype_1,
		max( startype_2 ) AS startype_2,
		max(startype_3) as startype_3,
		max( gender ) AS gender,
		max( age ) AS age,
		max( community_id ) AS community_id,
		max(
		concat( date_1, ' ', date_2 )) AS sign_date,
		max( location_1 ) AS location_1,
		max( location_2 ) AS location_2 
	FROM
		douyu.streamer 
	GROUP BY
		room_id 
	) st_t
	right JOIN 
	( SELECT room_id, max(COALESCE(follower_num_2019,follower_num_2018,follower_num_2017)) AS follower_num FROM douyu.follower_wide group by room_id ) fl_t 
	ON st_t.room_id = fl_t.room_id