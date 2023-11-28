with _raw_ev_charging_reports as (
    select *
    from {{ ref('stg_ev_charging_reports') }}
)

select session_ID session_id,
    Garage_ID garage_id,
    User_ID user_id,
    User_type user_type,
    Shared_ID shared_id,
    strptime(Start_plugin, '%d.%m.%Y %H:%M') start_plugin,
    Start_plugin_hour::INTEGER start_plugin_hour,
    strptime(End_plugout, '%d.%m.%Y %H:%M') end_plugout,
    End_plugout_hour::INTEGER end_plugout_hour,
    replace(El_kWh, ',', '.')::FLOAT el_kwh,
    replace(Duration_hours, ',', '.')::FLOAT duration_hours,
    month_plugin month_plugin,
    weekdays_plugin weekdays_plugin,
    Plugin_category plugin_category,
    Duration_category duration_category
from _raw_ev_charging_reports
