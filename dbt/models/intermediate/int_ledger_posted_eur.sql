{{ config(materialized='view') }}

-- Posted-only ledger lines converted to EUR, joined to account classification.
-- Same grain as stg_ledger (one row per ledger line), filtered to
-- journal_status = 'posted' — unposted/error journals never reach this layer,
-- so nothing downstream can accidentally include them.
with ledger as (

    select * from {{ ref('stg_ledger') }}

),

journal_entries as (

    select * from {{ ref('stg_journal_entries') }}

),

fx_rates as (

    select * from {{ ref('stg_fx_rates') }}

),

accounts as (

    select * from {{ ref('stg_accounts') }}

),

salesforce_customers as (

    select * from {{ ref('stg_salesforce_customers') }}

),

posted_ledger as (

    select ledger.*
    from ledger
    inner join journal_entries
        on ledger.journal_id = journal_entries.journal_id
    where journal_entries.journal_status = 'posted'

),

final as (

    select
        -- IDs
        posted_ledger.ledger_id,
        posted_ledger.journal_id,
        posted_ledger.gl_account_id,
        posted_ledger.customer_account_id,
        posted_ledger.entity_id,
        posted_ledger.territory_id,
        posted_ledger.business_unit_id,
        posted_ledger.consolidation_group_id,
        posted_ledger.ix_code_id,
        salesforce_customers.salesforce_customer_id,

        -- Strings
        posted_ledger.transaction_currency,
        accounts.account_type,
        accounts.reporting_group,

        -- Dates
        posted_ledger.ledger_date,

        -- Numbers
        posted_ledger.amount_original_currency,
        fx_rates.rate_to_eur,
        posted_ledger.amount_original_currency * fx_rates.rate_to_eur as amount_eur,

        -- Metadata
        accounts.is_pl_account,
        posted_ledger.is_adjustment_entry,
        posted_ledger.is_manual

    from posted_ledger
    left join fx_rates
        on date_trunc('month', posted_ledger.ledger_date)::date = fx_rates.fx_month_date
        and posted_ledger.transaction_currency = fx_rates.currency
    left join accounts
        on posted_ledger.gl_account_id = accounts.account_id
    left join salesforce_customers
        on posted_ledger.customer_account_id = salesforce_customers.customer_account_id

)

select * from final
