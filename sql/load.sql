create schema if not exists spc;
create or replace table spc.ev_charging_reports as (
    select session_ID session_id,
        Garage_ID garage_id,
        User_ID user_id,
        User_type user_type,
        Shared_ID shared_id,
        Start_plugin start_plugin,
        Start_plugin_hour start_plugin_hour,
        End_plugout end_plugout,
        End_plugout_hour end_plugout_hour,
        El_kWh el_kwh,
        Duration_hours duration_hours,
        month_plugin,
        weekdays_plugin,
        Plugin_category plugin_category,
        Duration_category duration_category
    from read_csv_auto(
        'data/ev_charging_reports.csv',
        sep=';',
        header=true,
        decimal_separator=',',
        nullstr='NA',
        timestampformat='%d.%m.%Y %H:%M', -- 21.12.2018 10:20
        types={
            'El_kWh': 'FLOAT',
            'Duration_hours': 'FLOAT',
            'Start_plugin': 'TIMESTAMP',
            'End_plugout': 'TIMESTAMP'
        }
    )
)
;
create or replace table spc.hourly_ev_loads_per_user as (
    select date_from,
        date_to,
        User_ID user_id,
        session_ID session_id,
        Synthetic_3_6kW synthetic_3_6kw,
        Synthetic_7_2kW synthetic_7_2kw,
        Flex_3_6kW flex_3_6kw,
        Flex_7_2kW flex_7_2kw
    from read_csv_auto(
        'data/hourly_ev_loads_per_user.csv',
        sep=';',
        header=true,
        decimal_separator=',',
        nullstr='NA',
        timestampformat='%d.%m.%Y %H:%M', -- 21.12.2018 10:20
        types={
            'session_ID': 'INTEGER',
            'Synthetic_3_6kW': 'FLOAT',
            'Synthetic_7_2kW': 'FLOAT',
            'Flex_3_6kW': 'FLOAT',
            'Flex_7_2kW': 'FLOAT'
        }
    )
)
;
create or replace table spc.hourly_ev_loads_aggregated as (
    with _aggregated_private as (
        select date_from::DATE date_from,
            daily_hour hour_from,
            Synthetic_3_6kW syntetic_3_6kw,
            Synthetic_7_2kW syntetic_7_2kw,
            Flex_3_6kW flex_3_6kw,
            Flex_7_2kW flex_7_2kw,
            n_private n
        from read_csv_auto(
            'data/hourly_ev_loads_aggregated_private.csv',
            sep=';',
            header=true,
            decimal_separator=',',
            nullstr='NA',
            timestampformat='%d.%m.%Y %H:%M', -- 21.12.2018 10:20
            types={
                'Synthetic_3_6kW': 'FLOAT',
                'Synthetic_7_2kW': 'FLOAT',
                'Flex_3_6kW': 'FLOAT',
                'Flex_7_2kW': 'FLOAT'
            }
        )
    ), _aggregated_shared as (
        select date_from::DATE date_from,
            daily_hour hour_from,
            Synthetic_3_6kW syntetic_3_6kw,
            Synthetic_7_2kW syntetic_7_2kw,
            Flex_3_6kW flex_3_6kw,
            Flex_7_2kW flex_7_2kw,
            n_shared n
        from read_csv_auto(
            'data/hourly_ev_loads_aggregated_shared.csv',
            sep=';',
            header=true,
            decimal_separator=',',
            nullstr='NA',
            timestampformat='%d.%m.%Y %H:%M', -- 21.12.2018 10:20
            types={
                'Synthetic_3_6kW': 'FLOAT',
                'Synthetic_7_2kW': 'FLOAT',
                'Flex_3_6kW': 'FLOAT',
                'Flex_7_2kW': 'FLOAT'
            }
        )
    )
    select *
    from (
        select 'Private' user_type, * from _aggregated_private
        union
        select 'Shared' user_type, * from _aggregated_shared
    )
    order by date_from, hour_from
)
;