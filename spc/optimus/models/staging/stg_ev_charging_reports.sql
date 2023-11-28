select *
from {{ source('warehouse', 'raw_ev_charging_reports') }}
