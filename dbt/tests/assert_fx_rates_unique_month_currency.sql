-- fails if any (month, currency) pair has more than one rate; a duplicate
-- here would silently corrupt every EUR conversion downstream.
select
    fx_month,
    currency,
    count(*) as rate_count
from {{ ref('stg_fx_rates') }}
group by 1, 2
having count(*) > 1
