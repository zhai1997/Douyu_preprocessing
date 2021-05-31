select 
startype_1,
startype_2,
startype_3,
count(distinct room_id) as dis_room
from 
douyu.feature_table
group by 
startype_1,
startype_2,
startype_3