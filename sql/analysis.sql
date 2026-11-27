#cau 1
SELECT ngay,
nhiet_min,
round((nhiet_min - avg(nhiet_min) over (partition by extract(month from ngay)))::numeric,1) as chenh_lech 
from raw_weather_daily
order by chenh_lech 
limit 5

#cau 2
with xh as (
select ngay,nhiet_max , extract(month from ngay) as thang,
row_number() over (partition by extract(month from ngay) order by nhiet_max DESC) as hang
from raw_weather_daily 
)
select ngay, nhiet_max , thang
from xh 
where hang = 1

order by thang;
