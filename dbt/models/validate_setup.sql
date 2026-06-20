{{
    config(
        alias="validate_setup",
        materialized="table",
    )
}}

SELECT 1 AS validation_check
