{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        journal_id,

        -- Strings
        source_system,
        posted_by,
        status as journal_status,

        -- Timestamps
        posted_at

    from {{ source('mock_data', 'journal_entries') }}

)

select * from final
