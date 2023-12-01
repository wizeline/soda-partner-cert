select *
from {{ source('kaggle', 'raw_hourly_ev_loads') }}
