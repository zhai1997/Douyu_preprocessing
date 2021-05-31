create table if not exists debug_t as 
select 
*, 
0 as myrank
from douyu.feature_table
where startype_1='娱乐天地'
order by follower_num desc;
set @r:=0;
update debug_t set myrank=(@r:=@r+1);
select * from 
(select follower_num,myrank from debug_t 
where follower_num is not null) a join
(select 0.1*count(distinct room_id) as total_num from debug_t
where follower_num is not null) b
where myrank>total_num-1 and myrank<total_num+1