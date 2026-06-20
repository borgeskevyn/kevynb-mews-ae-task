{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        business_unit as business_unit_id,

        -- Strings
        description as business_unit_description,
        unit_type,
        manager

    from {{ source('mock_data', 'business_units') }}

)

select * from final
