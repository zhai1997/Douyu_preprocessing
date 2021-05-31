create  database if not exists douyu;
use douyu;
create table if not exists dt(
	user_id char(11),
	room_id char(11),
	content varchar(200),
	if_fan int,
	if_vip int,
	time varchar(20)
)DEFAULT charset = utf8;
create table if not exists streamer(
	room_id char(11),
	startype_1 varchar(20),
	startype_2 varchar(20),
	startype_3 varchar(20),
	gender int,
	age int,
	community_id bigint,
	date_1 varchar(20),
	date_2 varchar(20),
	location_1 varchar(20),
	location_2 varchar(20)
)DEFAULT charset = utf8;
create table if not exists start_live_only2019(
	live_date char(8),
	room_id char(11),
	start_time bigint,
	end_time bigint,
	roomtype_1 varchar(10),
	roomtype_2 varchar(10),
	roomtype_3 varchar(10)
)DEFAULT charset = utf8;