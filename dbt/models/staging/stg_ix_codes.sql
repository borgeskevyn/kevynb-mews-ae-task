{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        ix_code as ix_code_id,

        -- Strings
        description as ix_code_description,
        category as ix_code_category,

        -- Dates
        created_date as ix_code_created_date,

        -- Metadata
        is_active

    from {{ source('mock_data', 'ix_codes') }}

)

select * from final
