{{ config(materialized='view') }}

-- account_code (GL account, joins to stg_accounts.account_id) and account_number
-- (customer account, joins to stg_salesforce_customers / stg_business_central_customers
-- via customer_account_id) are two distinct identifiers in the source; renamed
-- explicitly to prevent the two from being confused downstream.
with final as (

    select
        -- IDs
        id as ledger_id,
        journal_id,
        account_code as gl_account_id,
        account_number as customer_account_id,
        entity_code as entity_id,
        territory as territory_id,
        business_unit as business_unit_id,
        consolidation_group as consolidation_group_id,
        ix_code as ix_code_id,

        -- Strings
        currency as transaction_currency,

        -- Dates
        date as ledger_date,

        -- Numbers
        amount as amount_original_currency,

        -- Metadata
        is_adjustment_entry,
        is_manual

    from {{ source('mock_data', 'ledger') }}

)

select * from final
