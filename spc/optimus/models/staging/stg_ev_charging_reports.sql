select *
from {{ source('kaggle', 'raw_ev_charging_reports') }}
