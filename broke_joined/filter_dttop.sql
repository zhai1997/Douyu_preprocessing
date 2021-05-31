SET global max_heap_table_size=536870912000; 
SET GLOBAL tmp_table_size=536870912000;
create table if not exists dt_top_2019 as 
select *from 
dt_top 
where substr(time,1,7)='2019-12'