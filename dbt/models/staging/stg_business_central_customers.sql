{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        id as business_central_customer_id,
        account_number as customer_account_id,

        -- Strings
        currency as customer_currency,
        country_code

    from {{ source('mock_data', 'business_central_global_customers') }}

)

select * from final
