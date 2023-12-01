{% set timestamp_format = '%d.%m.%Y %H:%M' %}

with _raw_hourly_ev_loads as (
    select *
    from {{ ref('stg_hourly_ev_loads') }}
)
select {{ strptime('date_from', timestamp_format) }} date_from,
	{{ strptime('date_to', timestamp_format) }} date_to,
	User_ID user_id,
	CAST(session_ID AS INTEGER) session_id,
	CAST(replace(Synthetic_3_6kW, ',', '.') AS NUMERIC) synthetic_3_6kw,
	CAST(replace(Synthetic_7_2kW, ',', '.') AS NUMERIC) synthetic_7_2kw,
	CAST(replace(Flex_3_6kW, ',', '.') AS NUMERIC) flex_3_6kw,
	CAST(replace(Flex_7_2kW, ',', '.') AS NUMERIC) flex_7_2kw
from _raw_hourly_ev_loads
