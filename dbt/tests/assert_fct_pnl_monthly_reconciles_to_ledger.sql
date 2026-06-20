-- fails if the mart's total EUR P&L activity doesn't tie back to the
-- intermediate layer's total — catches drift introduced by the mart's
-- aggregation logic (e.g. wrong filter, wrong group-by) that unit tests on
-- individual columns wouldn't reveal.
with ledger_total as (

    select round(sum(amount_eur)::numeric, 2) as total_eur
    from {{ ref('int_ledger_posted_eur') }}
    where is_pl_account

),

mart_total as (

    select round(sum(revenue_eur + expense_eur)::numeric, 2) as total_eur
    from {{ ref('fct_pnl_monthly') }}

)

select
    ledger_total.total_eur as expected_total_eur,
    mart_total.total_eur as actual_total_eur
from ledger_total
cross join mart_total
where ledger_total.total_eur != mart_total.total_eur
