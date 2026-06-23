{{ config(materialized='table') }}

-- Monthly P&L by entity, territory, business unit, consolidation group,
-- IX code and Salesforce customer, in EUR. Only is_pl_account = true lines
-- are included — Balance Sheet accounts (Asset/Liability, e.g. Cash/Accounts
-- Payable) are out of scope for a P&L view.
with ledger_eur as (

    select * from {{ ref('int_ledger_posted_eur') }}
    where is_pl_account

),

aggregated as (

    select
        -- IDs
        entity_id,
        territory_id,
        business_unit_id,
        consolidation_group_id,
        ix_code_id,
        salesforce_customer_id,

        -- Dates
        date_trunc('month', ledger_date)::date as pnl_month,

        -- Numbers
        sum(case when account_type = 'Revenue' then amount_eur else 0 end) as revenue_eur,
        sum(case when account_type = 'Expense' then amount_eur else 0 end) as expense_eur,
        count(*) as ledger_line_count

    from ledger_eur
    group by 1, 2, 3, 4, 5, 6, 7

),

final as (

    select
        -- IDs
        entity_id,
        territory_id,
        business_unit_id,
        consolidation_group_id,
        ix_code_id,
        salesforce_customer_id,

        -- Dates
        pnl_month,

        -- Numbers
        revenue_eur,
        expense_eur,
        revenue_eur - expense_eur as net_eur,
        ledger_line_count

    from aggregated

)

select * from final
