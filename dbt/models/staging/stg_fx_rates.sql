{{ config(materialized='view') }}

with final as (

    select
        -- Strings
        month as fx_month,
        currency,

        -- Dates
        to_date(month || '-01', 'YYYY-MM-DD') as fx_month_date,

        -- Numbers
        rate_to_eur

    from {{ source('mock_data', 'fx_rates') }}

)

select * from final
