SET group_concat_max_len=10240000000;
Select 
centile(0.01,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_01,
centile(0.05,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_05,
centile(0.10,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_10,
centile(0.25,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_25,
centile(0.50,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_50,
centile(0.75,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_75,
centile(0.90,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_90,
centile(0.95,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_95,
centile(0.99,GROUP_CONCAT(follower_num ORDER BY follower_num SEPARATOR ',')) as quartile_99
FROM feature_table
where follower_num is not null
