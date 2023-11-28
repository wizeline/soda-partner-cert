select *
from {{ source('warehouse', 'raw_hourly_ev_loads') }}
