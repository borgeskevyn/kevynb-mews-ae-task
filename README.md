# Mews FP&A Data Model

A dbt project that turns a mock general ledger (plus CRM and ERP customer
records) into a tested, documented star schema for monthly P&L reporting.

## Repo layout

```
.
├── build.sh / clean.sh       # spin up / tear down Postgres + mock data + API server (Docker)
├── src/
│   ├── build_mock.py         # generates src/data/mock_data.json (Salesforce, BC, ledger, FX, etc.)
│   ├── init_postgres.py      # creates tables and loads mock_data.json into Postgres
│   └── fno_data__server.js   # small Express API in front of the same data (not used by dbt)
├── dbt/
│   ├── models/
│   │   ├── sources/          # src_tables.yml — declares the raw mock_data tables
│   │   ├── staging/          # stg_* — 1:1 with sources, renamed/typed, no business logic
│   │   ├── intermediate/     # int_* — joins/derives across staging models
│   │   └── marts/            # fct_* — the reporting-facing star schema
│   ├── tests/                 # singular (hand-written) data tests
│   └── dbt_project.yml
├── docs/
│   └── fct_pnl_monthly_exploration.md  # ad hoc analysis of the fact table output
└── pyproject.toml            # dbt-postgres + dev tooling, managed via uv
```

## Architecture

Three-layer dbt convention, each layer only ever reading from the layer below:

```
sources (mock_data.*)
  └─ staging (stg_*)            1 row in  → 1 row out, renamed + typed, no joins
       └─ intermediate (int_*)  joins, filters, currency conversion
            └─ marts (fct_*)    aggregated, reporting-grain star schema
```

**Staging** (`models/staging/`) — one model per source table. Each one just
renames source columns to consistent business keys (e.g. `account_code` →
`gl_account_id`, `account_number` → `customer_account_id`) and casts types.
No joins, no filtering, no aggregation — these are 1:1 mirrors of the source
tables so every downstream model has a single, stable place to depend on.

**Intermediate** (`models/intermediate/`) — `int_ledger_posted_eur` is the
one model here. It:
- filters `stg_ledger` down to `journal_status = 'posted'` lines only,
- converts `amount_original_currency` to EUR via `stg_fx_rates`,
- joins `stg_accounts` for P&L classification (`account_type`, `is_pl_account`),
- left-joins `stg_salesforce_customers` on `customer_account_id` to attach a
  CRM customer where one exists.

Same grain as `stg_ledger` (one row per posted ledger line) — nothing is
aggregated yet, so this is the layer to query if you need ledger-line detail
(e.g. `gl_account_id`, `customer_account_id`) that the mart below rolls up.

**Marts** (`models/marts/`) — `fct_pnl_monthly`, the star-schema fact table.
Grain: one row per `(entity, territory, business_unit, consolidation_group,
ix_code, salesforce_customer, month)`. Filters to `is_pl_account` (Revenue/
Expense accounts only — Balance Sheet activity is out of scope by design) and
sums `amount_eur` into `revenue_eur` / `expense_eur` / `net_eur`.

### Why this grain

The fact table carries every dimension key that's available at the ledger
line's natural grain and has a uniquely-keyed dimension table to join to —
`entity_id`, `territory_id`, `business_unit_id`, `consolidation_group_id`,
`ix_code_id`, `salesforce_customer_id` — so it behaves like a conventional
star-schema fact rather than a fixed, narrow rollup. Two FKs were deliberately
left out:

- `gl_account_id` / `customer_account_id` (raw account/customer numbers) —
  adding these would push the grain back to ~1 row per ledger line, which
  defeats the point of a monthly mart. Use `int_ledger_posted_eur` directly
  for that level of detail.
- Business Central customer ID — `stg_business_central_customers.customer_account_id`
  is **not unique** in the source (a small number of accounts have two BC
  records), so joining it directly would fan out ledger lines. Salesforce's
  equivalent key *is* unique (`unique` + `not_null` tested), which is why only
  the Salesforce join made it into `int_ledger_posted_eur` / `fct_pnl_monthly`.

## Naming conventions

- `stg_<source>` / `int_<purpose>` / `fct_<purpose>` prefixes by layer.
- Every foreign/primary key column ends in `_id` (`entity_id`,
  `salesforce_customer_id`, …) regardless of what the source called it —
  e.g. `account_code` and `account_number` are two distinct identifiers in the
  raw ledger and are renamed to `gl_account_id` / `customer_account_id`
  specifically so they can't be confused downstream.
- Currency-converted amounts are suffixed `_eur` (`amount_eur`, `revenue_eur`)
  to make it unambiguous which figures are post-FX-conversion.
- Model files follow the `-- IDs / -- Strings / -- Dates / -- Numbers /
  -- Metadata` column grouping convention throughout, so every `select` reads
  the same way regardless of model.

## Testing strategy

Two kinds of tests, doing different jobs:

**Generic (schema) tests**, declared in each model's `yml`:
- `unique` / `not_null` on primary keys (`ledger_id`, `salesforce_customer_id`, …).
- `relationships` on every foreign key, pointed at its dimension table — this
  is what would catch an orphaned `business_unit_id` or a typo'd `ix_code_id`.
  Keys that are allowed to be unmatched (`salesforce_customer_id`, since not
  every ledger line resolves to a CRM record) get `relationships` without
  `not_null`, so a null is fine but a *non-null mismatch* still fails.
- `accepted_values` (e.g. `journal_status` in `posted/unposted/error`).
- `not_null` on `amount_eur` — by design. The FX and account joins in
  `int_ledger_posted_eur` are `left join`s, so a missing FX rate or an
  unrecognized GL account doesn't silently drop the line; it surfaces as a
  failing `not_null` test instead.

**Singular tests**, hand-written in `dbt/tests/`:
- `assert_fct_pnl_monthly_reconciles_to_ledger.sql` — sums total EUR P&L
  activity at the mart and at the intermediate layer and fails if they
  diverge. Catches aggregation bugs (wrong filter, wrong group-by) that
  per-column tests wouldn't see.
- `assert_int_ledger_posted_eur_no_fanout.sql` — compares row counts before
  and after the FX/account/Salesforce joins. Any join that unexpectedly
  duplicates or drops rows fails this immediately, before it can silently
  double-count revenue downstream.
- `assert_fx_rates_unique_month_currency.sql` — guards the FX join key itself
  (one rate per currency per month), since a duplicate would also fan out
  `int_ledger_posted_eur`.

Run everything with `dbt build` (runs models + tests together) or `dbt test`
against an already-built target.

## Lineage

```
mock_data.salesforce_customers ─────┐
mock_data.ledger ──┐                │
mock_data.journal_entries ─┼─ stg_ledger ─┬─ int_ledger_posted_eur ─→ fct_pnl_monthly
mock_data.fx_rates ─────────┤            │ (+ stg_fx_rates, stg_accounts,
mock_data.accounts ─────────┘            │  stg_salesforce_customers)
                                          │
mock_data.entity_codes ─→ stg_entity_codes ┐
mock_data.territories ─→ stg_territories   ├─ (relationships tests only —
mock_data.business_units ─→ stg_business_units │  these don't feed the mart,
mock_data.consolidation_groups ─→ stg_consolidation_groups │ they validate FKs against it)
mock_data.ix_codes ─→ stg_ix_codes ─────────┘
```

For the interactive, clickable version: `dbt docs generate && dbt docs serve`
from the `dbt/` directory — this renders the full DAG plus every column
description and test from the model `yml` files.

## Running it locally

**Option A — Docker (as intended by `build.sh`):**
```bash
sh build.sh   # builds Postgres + loads mock data + starts API server + dbt debug
```

**Option B — local Postgres (used to validate this branch, since the sandbox
had no Docker daemon):**
```bash
# 1. Postgres running locally, with a produser/prodpassword/proddb matching
#    src/init_postgres.py's hardcoded connection settings
# 2. uv sync --dev
# 3. uv run python3 src/build_mock.py        # writes src/data/mock_data.json
# 4. uv run python3 src/init_postgres.py      # loads it into Postgres
# 5. create dbt/profiles.yml (gitignored) pointing at that Postgres instance
# 6. cd dbt && DBT_PROFILES_DIR=. uv run dbt build
```

`src/data/` is gitignored — `mock_data.json` is regenerated by `build_mock.py`
on every run, so it's not committed.

## Further reading

[`docs/fct_pnl_monthly_exploration.md`](docs/fct_pnl_monthly_exploration.md) —
ad hoc analysis of `fct_pnl_monthly`'s output (revenue/expense/margin by
entity, territory, business unit, consolidation group, IX code and Salesforce
customer), run against the mock dataset described above.
