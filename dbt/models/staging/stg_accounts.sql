{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        account_code as account_id,

        -- Strings
        account_name,
        account_type,
        reporting_group,

        -- Metadata
        is_pl_account

    from {{ source('mock_data', 'accounts') }}

)

select * from final
