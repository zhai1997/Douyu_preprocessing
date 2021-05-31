SET SESSION max_heap_table_size=536870912000; 
SET SESSION tmp_table_size=536870912000; 
create table if not exists douyu.follower_wide as
with follower_2017 as (
select
room_id, 
follower_num as follower_num_2017
from douyu.follower
where date='20170612'
),
follower_2018 as(
select 
room_id, 
follower_num as follower_num_2018
from douyu.follower
where date='20180101'
),
follower_2019 as(
select 
room_id,
follower_num as follower_num_2019
from douyu.follower
where date='20191231'
),
follower_1718 as(
select 
follower_2017.room_id,
follower_num_2017,
follower_num_2018
from 
follower_2017
left join 
follower_2018
on follower_2017.room_id=follower_2018.room_id

union

select 
follower_2018.room_id,
follower_num_2017,
follower_num_2018
from 
follower_2017
right join 
follower_2018
on follower_2017.room_id=follower_2018.room_id
)

select 
follower_1718.room_id,
follower_num_2017,
follower_num_2018,
follower_num_2019
from 
follower_1718
left join 
follower_2019
on follower_1718.room_id=follower_2019.room_id

union

select 
follower_2019.room_id,
follower_num_2017,
follower_num_2018,
follower_num_2019
from 
follower_1718
right join 
follower_2019
on follower_1718.room_id=follower_2019.room_id













