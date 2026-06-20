{{ config(materialized='view') }}

with final as (

    select
        -- IDs
        consolidation_group as consolidation_group_id,
        lead_entity as lead_entity_id,

        -- Strings
        description as consolidation_group_description,
        group_type

    from {{ source('mock_data', 'consolidation_groups') }}

)

select * from final
