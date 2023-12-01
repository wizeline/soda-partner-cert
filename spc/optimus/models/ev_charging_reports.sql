{% set timestamp_format = '%d.%m.%Y %H:%M' %}
with _raw_ev_charging_reports as (
    select *
    from {{ ref('stg_ev_charging_reports') }}
)

select session_ID session_id,
    Garage_ID garage_id,
    User_ID user_id,
    User_type user_type,
    Shared_ID shared_id,
    {{ strptime('Start_plugin', timestamp_format) }} start_plugin,
    CAST(Start_plugin_hour AS INTEGER) start_plugin_hour,
    {{ strptime('End_plugout', timestamp_format) }} end_plugout,
    CAST(End_plugout_hour AS INTEGER) end_plugout_hour,
    CAST(replace(El_kWh, ',', '.') AS NUMERIC) el_kwh,
    CAST(replace(Duration_hours, ',', '.') AS NUMERIC) duration_hours,
    month_plugin month_plugin,
    weekdays_plugin weekdays_plugin,
    Plugin_category plugin_category,
    Duration_category duration_category
from _raw_ev_charging_reports
