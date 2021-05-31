select 
count(distinct if(follower_num_2019 is not null, room_id, null)) as num_2019,
count(distinct if(follower_num_2018 is not null, room_id, null)) as num_2018,
count(distinct if(follower_num_2017 is not null, room_id, null)) as num_2017,
count(distinct room_id) as total_num
from 
follower_wide