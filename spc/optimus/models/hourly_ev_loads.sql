with _raw_hourly_ev_loads as (
    select *
    from {{ ref('stg_hourly_ev_loads') }}
)
select strptime(date_from, '%d.%m.%Y %H:%M') date_from,
	strptime(date_to, '%d.%m.%Y %H:%M') date_to,
	User_ID user_id,
	session_ID::INTEGER session_id,
	replace(Synthetic_3_6kW, ',', '.')::FLOAT synthetic_3_6kw,
	replace(Synthetic_7_2kW, ',', '.')::FLOAT synthetic_7_2kw,
	replace(Flex_3_6kW, ',', '.')::FLOAT flex_3_6kw,
	replace(Flex_7_2kW, ',', '.')::FLOAT flex_7_2kw
from _raw_hourly_ev_loads
