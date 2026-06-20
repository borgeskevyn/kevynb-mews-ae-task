{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        territory as territory_id,

        -- Strings
        description as territory_description,
        region,
        country_group

    from {{ source('mock_data', 'territories') }}

)

select * from final
