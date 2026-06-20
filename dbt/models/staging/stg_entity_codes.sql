{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        entity_code as entity_id,

        -- Strings
        description as entity_description,

        -- Dates
        created_at as entity_created_date

    from {{ source('mock_data', 'entity_codes') }}

)

select * from final
