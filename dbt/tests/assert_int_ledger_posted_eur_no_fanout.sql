-- fails if the FX/accounts joins in int_ledger_posted_eur produced more or
-- fewer rows than there are posted ledger lines — a silent fan-out here would
-- double-count (or drop) amounts in every downstream P&L total.
with posted_ledger_count as (

    select count(*) as row_count
    from {{ ref('stg_ledger') }} as ledger
    inner join {{ ref('stg_journal_entries') }} as journal_entries
        on ledger.journal_id = journal_entries.journal_id
    where journal_entries.journal_status = 'posted'

),

int_count as (

    select count(*) as row_count
    from {{ ref('int_ledger_posted_eur') }}

)

select
    posted_ledger_count.row_count as expected_row_count,
    int_count.row_count as actual_row_count
from posted_ledger_count
cross join int_count
where posted_ledger_count.row_count != int_count.row_count
