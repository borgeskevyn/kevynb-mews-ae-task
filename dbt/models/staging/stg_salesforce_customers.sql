{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        id as salesforce_customer_id,
        account_number as customer_account_id,

        -- Strings
        name as customer_name,
        billing_country,

        -- Numbers
        capacity_s,
        capacity_m,
        capacity_l,

        -- Metadata
        is_deleted

    from {{ source('mock_data', 'salesforce_customers') }}

)

select * from final
