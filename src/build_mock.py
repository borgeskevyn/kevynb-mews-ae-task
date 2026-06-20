"""
This script generates mock data for Salesforce and Business Central, including a general ledger.

Created by: Mews.FnO.Data
Last updated: 2025-07-09

Functions:
    generate_hotel_name: Generate a random hotel name.
    build_salesforce: Build a Salesforce customer record, with some missing fields at random.
    build_businesscentral: Build Business Central customers, including some not in Salesforce.
    build_ledger: Build a general ledger for BC customers with IX codes for revenue.
    build_fx_rates: Build a table of FX rates for all currencies (except EUR, which is always 1.0)
    routine: Generate and export all mock data.

Variables:
    CURRENCIES: List of currencies.
    IX_CODES: List of IX codes.
    ACCOUNT_NUMBER_RANGE: Range of account numbers.
    COUNTRY_CODES: List of country codes.
    SALESFORCE_ID_LENGTH: Length of Salesforce ID.
    ADJECTIVES: List of adjectives.
    NOUNS: List of nouns.

Usage:
    $ python build_mock.py
"""

from pathlib import Path
import uuid
import json
import random
import typing
import datetime

# VARIABLES

CURRENCIES: list = [
    "EUR",
    "CZK",
    "USD",
    "GBP",
    "JPY",
    "CAD",
    "AUD",
    "CHF",
    "SEK",
    "NOK",
]

IX_CODES: list[float] = [1, 1.74, 2, 2.23, 3, 3.12, 4, 4.98, 5]

ACCOUNT_NUMBER_RANGE: dict = {"min": 10001, "max": 12000}

COUNTRY_CODES: list[str] = [
    "CZ",
    "DE",
    "FR",
    "GB",
    "IT",
    "PL",
    "SK",
    "US",
    "JP",
    "CA",
    "AU",
    "CH",
    "SE",
    "NO",
]

SALESFORCE_ID_LENGTH: int = 18

ADJECTIVES: list[str] = [
    "Luxurious",
    "Elegant",
    "Charming",
    "Cozy",
    "Modern",
    "Stylish",
    "Rustic",
    "Historic",
    "Boutique",
    "Quaint",
    "Secluded",
    "Romantic",
    "Peaceful",
    "Tranquil",
    "Serene",
    "Idyllic",
    "Picturesque",
    "Enchanting",
    "Enchanted",
    "Magical",
    "Mystical",
    "Whimsical",
    "Dreamy",
    "Fantastical",
    "Fairytale",
    "Heavenly",
    "Paradise",
    "Tropical",
    "Exotic",
    "Sunny",
    "Beachfront",
    "Oceanfront",
    "Seaside",
    "Mountain",
    "Alpine",
    "Forest",
    "Woodland",
    "Riverside",
    "Lakeside",
    "Countryside",
    "Vineyard",
    "Farmhouse",
    "Plantation",
    "Heritage",
    "Colonial",
    "Antique",
    "Vintage",
    "Retro",
    "Bohemian",
]
NOUNS: list[str] = [
    "Hotel",
    "Resort",
    "Inn",
    "Lodge",
    "Retreat",
    "Hideaway",
    "Haven",
    "Sanctuary",
    "Oasis",
    "Refuge",
    "Paradise",
    "Nest",
    "Hearth",
    "Haven",
    "Shelter",
    "Cottage",
    "Cabin",
    "Chalet",
    "Bungalow",
    "Villa",
    "Mansion",
    "Manor",
    "Estate",
    "Palace",
    "Castle",
    "Chateau",
    "Fortress",
    "Keep",
    "Tower",
    "Citadel",
    "Stronghold",
    "Fort",
    "Bastion",
    "Garrison",
    "Outpost",
]

ENTITY_CODES = ["ENT1", "ENT2", "ENT3"]
TERRITORIES = ["CZ", "DE", "FR", "GB", "US"]
BUSINESS_UNITS = ["BU1", "BU2", "BU3"]
CONSOLIDATION_GROUPS = ["GroupA", "GroupB"]

ACCOUNT_DIM = [
    {
        "account_code": "4000",
        "account_name": "Revenue A",
        "account_type": "Revenue",
        "reporting_group": "Revenue",
        "is_pl_account": True,
    },
    {
        "account_code": "4001",
        "account_name": "Revenue B",
        "account_type": "Revenue",
        "reporting_group": "Revenue",
        "is_pl_account": True,
    },
    {
        "account_code": "5000",
        "account_name": "Expense A",
        "account_type": "Expense",
        "reporting_group": "Expenses",
        "is_pl_account": True,
    },
    {
        "account_code": "1000",
        "account_name": "Cash",
        "account_type": "Asset",
        "reporting_group": "Balance Sheet",
        "is_pl_account": False,
    },
    {
        "account_code": "2000",
        "account_name": "Accounts Payable",
        "account_type": "Liability",
        "reporting_group": "Balance Sheet",
        "is_pl_account": False,
    },
]

# FUNCTIONS


def generate_hotel_name() -> str:
    """
    Generate a random hotel name by combining a random adjective and noun.

    Returns:
        str: A randomly generated hotel name.

    Example:
        >>> generate_hotel_name()
        'Luxurious Resort'
    """
    adjective: str = random.choice(ADJECTIVES)
    noun: str = random.choice(NOUNS)

    return f"{adjective} {noun}"


def build_salesforce(account_number: int) -> dict[str, typing.Any]:
    """
    Build a Salesforce customer record.
    Some fields (name, billing country, capacities) may be missing at random.

    Returns:
        dict[str, typing.Any]: A Salesforce customer record.

    Example:
        >>> build_salesforce(10001)
        {
            "Id": "f5b9c5b5-7f9a-4b7b-8b4d-0b3b8f7b1c2d",
            "IsDeleted": False,
            "AccountNumber": 10001,
            "Name": "Luxurious Resort",
            "BillingCountry": "CZ",
            "CapacityS": 42,
            "CapacityM": 38,
            "CapacityL": 16
        }
    """
    salesforce_id: str = str(uuid.uuid4()).replace("-", "")[:SALESFORCE_ID_LENGTH]
    is_deleted: bool = random.randrange(0, 100, 1) == 73
    name: typing.Optional[str] = generate_hotel_name()
    billing_country: typing.Optional[str] = random.choice(COUNTRY_CODES)
    capacity_s: typing.Optional[int] = random.randint(1, 100)
    capacity_m: typing.Optional[int] = random.randint(1, 100)
    capacity_l: typing.Optional[int] = random.randint(1, 100)

    if random.randint(1, 250) == 1:
        name = None
    if random.randint(1, 250) == 1:
        billing_country = None
    if random.randint(1, 250) == 1:
        capacity_s = None
    if random.randint(1, 250) == 1:
        capacity_m = None
    if random.randint(1, 250) == 1:
        capacity_l = None

    salesforce_payload: dict[str, typing.Any] = {
        "id": salesforce_id,
        "is_deleted": is_deleted,
        "account_number": account_number,
        "name": name,
        "billing_country": billing_country,
        "capacity_s": capacity_s,
        "capacity_m": capacity_m,
        "capacity_l": capacity_l,
    }

    return salesforce_payload


def build_businesscentral(
    account_number: int, sf_account_numbers: set[int]
) -> dict[str, str]:
    """
    Build a Business Central global customer.
    ~10% of customers will have account numbers not in Salesforce.

    Returns:
        dict[str, str]: A Business Central global customer record.

    Example:
        >>> build_businesscentral(10001)
        {
            "Id": "f5b9c5b5-7f9a-4b7b-8b4d-0b3b8f7b1c2d",
            "AccountNumber": 10001,
            "Currency": "EUR",
            "CountryCode": "CZ"
        }
    """

    if random.random() < 0.10:
        while True:
            fake_account = random.randint(
                ACCOUNT_NUMBER_RANGE["min"], ACCOUNT_NUMBER_RANGE["max"] + 1000
            )
            if fake_account not in sf_account_numbers:
                account_number = fake_account
                break
    businesscentral_id: str = str(uuid.uuid4())
    currency: str = random.choice(CURRENCIES)
    country_code: str = random.choice(COUNTRY_CODES)

    businesscentral_payload: dict[str, str] = {
        "id": businesscentral_id,
        "account_number": account_number,
        "currency": currency,
        "country_code": country_code,
    }

    return businesscentral_payload


def build_accounts_table() -> list[dict[str, typing.Any]]:
    """
    Build account dimension table.
    """
    return ACCOUNT_DIM


def build_journal_entries(num_entries: int) -> list[dict[str, typing.Any]]:
    """
    Build journal entry metadata table.
    """
    statuses = ["posted", "unposted", "error"]
    sources = ["BC"]
    posted_bys = ["system", "user", "api"]
    journal_entries = []
    for _ in range(num_entries):
        journal_id = str(uuid.uuid4())
        entry = {
            "journal_id": journal_id,
            "source_system": random.choice(sources),
            "posted_by": random.choice(posted_bys),
            "status": random.choices(statuses, weights=[0.85, 0.1, 0.05])[0],
            "posted_at": (
                datetime.datetime.now()
                - datetime.timedelta(days=random.randint(0, 150))
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }
        journal_entries.append(entry)
    return journal_entries


# Map for correct region/country_group for each territory
TERRITORY_META = {
    "CZ": {"region": "EMEA", "country_group": "EU"},
    "DE": {"region": "EMEA", "country_group": "EU"},
    "FR": {"region": "EMEA", "country_group": "EU"},
    "GB": {"region": "EMEA", "country_group": "Non-EU"},
    "IT": {"region": "EMEA", "country_group": "EU"},
    "PL": {"region": "EMEA", "country_group": "EU"},
    "SK": {"region": "EMEA", "country_group": "EU"},
    "US": {"region": "AMER", "country_group": "Non-EU"},
    "JP": {"region": "APAC", "country_group": "Non-EU"},
    "CA": {"region": "AMER", "country_group": "Non-EU"},
    "AU": {"region": "APAC", "country_group": "Non-EU"},
    "CH": {"region": "EMEA", "country_group": "Non-EU"},
    "SE": {"region": "EMEA", "country_group": "EU"},
    "NO": {"region": "EMEA", "country_group": "Non-EU"},
}


def build_territories_table(territories: list[str]) -> list[dict[str, typing.Any]]:
    """Builds territories dimension table with correct region/country_group."""
    return [
        {
            "territory": terr,
            "description": f"Territory {terr} description",
            "region": TERRITORY_META.get(terr, {}).get("region", "UNKNOWN"),
            "country_group": TERRITORY_META.get(terr, {}).get(
                "country_group", "UNKNOWN"
            ),
        }
        for terr in territories
    ]


def build_entity_codes_table(entity_codes: list[str]) -> list[dict[str, typing.Any]]:
    """Builds entity_codes dimension table with dummy metadata."""
    return [
        {
            "entity_code": code,
            "description": f"Entity {code} description",
            "created_at": str(datetime.date(2020, 1, random.randint(1, 28))),
        }
        for code in entity_codes
    ]


def build_business_units_table(
    business_units: list[str],
) -> list[dict[str, typing.Any]]:
    """Builds business_units dimension table with dummy metadata."""
    return [
        {
            "business_unit": bu,
            "description": f"Business Unit {bu} description",
            "unit_type": random.choice(["Sales", "Service", "Admin"]),
            "manager": f"Manager {random.randint(1, 10)}",
        }
        for bu in business_units
    ]


def build_consolidation_groups_table(
    consolidation_groups: list[str],
) -> list[dict[str, typing.Any]]:
    """Builds consolidation_groups dimension table with dummy metadata."""
    return [
        {
            "consolidation_group": cg,
            "description": f"Consolidation Group {cg} description",
            "group_type": random.choice(["Internal", "External"]),
            "lead_entity": random.choice(["ENT1", "ENT2", "ENT3"]),
        }
        for cg in consolidation_groups
    ]


def build_ix_codes_table(ix_codes: list[int]) -> list[dict[str, typing.Any]]:
    """Builds IX codes dimension table with dummy metadata."""
    return [
        {
            "ix_code": ix,
            "description": f"IX Code {ix} description",
            "category": random.choice(["Revenue", "Service", "Product", "Region"]),
            "is_active": random.choice([True, True, True, False]),  # 75% active
            "created_date": str(datetime.date(2020, random.randint(1, 12), random.randint(1, 28))),
        }
        for ix in ix_codes
    ]


def build_ledger(
    bc_customers: list[dict[str, typing.Any]],
    journal_entries: list[dict[str, typing.Any]],
    accounts: list[dict[str, typing.Any]],
) -> list[dict[str, typing.Any]]:
    """
    Build a general ledger for BC customers with audit fields and entity structure.
    """
    ledger: list[dict[str, typing.Any]] = []
    now = datetime.datetime.now()
    months = []
    for i in range(5):
        month = (now - datetime.timedelta(days=30 * i)).replace(day=1)
        months.append(month.strftime("%Y-%m"))

    for customer in bc_customers:
        account_number = customer["account_number"]
        entity_code = random.choice(ENTITY_CODES)
        territory = random.choice(TERRITORIES)
        business_unit = random.choice(BUSINESS_UNITS)
        consolidation_group = random.choice(CONSOLIDATION_GROUPS)
        used_months = random.sample(months, k=random.randint(1, len(months)))
        for month in used_months:
            used_accounts = random.sample(accounts, k=random.randint(1, len(accounts)))
            for acc in used_accounts:
                year, m = map(int, month.split("-"))
                day = random.randint(1, 28)
                date = f"{year}-{m:02d}-{day:02d}"
                currency = random.choice(CURRENCIES)
                amount = round(random.uniform(100, 10000), 2)
                ix_code = random.choice(IX_CODES)
                journal_entry = random.choice(journal_entries)
                journal_id = journal_entry["journal_id"]
                is_adjustment_entry = random.random() < 0.05
                is_manual = random.random() < 0.1
                ledger.append(
                    {
                        "id": str(uuid.uuid4()),
                        "journal_id": journal_id,
                        "account_number": account_number,
                        "account_code": acc["account_code"],
                        "date": date,
                        "currency": currency,
                        "amount": amount,
                        "ix_code": ix_code,
                        "entity_code": entity_code,
                        "territory": territory,
                        "business_unit": business_unit,
                        "consolidation_group": consolidation_group,
                        "is_adjustment_entry": is_adjustment_entry,
                        "is_manual": is_manual,
                    }
                )
    return ledger


def build_fx_rates() -> list[dict[str, typing.Any]]:
    """
    Build a table of FX rates for all currencies (except EUR, which is always 1.0)
    for each of the last 5 months. Each entry: {"month": "YYYY-MM", "currency": "XXX", "rate_to_eur": float}

    Returns:
        list[dict[str, typing.Any]]: A list of FX rates for the last 5 months.

    Example:
        >>> build_fx_rates()
        [
            {"month": "2025-06", "currency": "USD", "rate_to_eur": 1.08},
            {"month": "2025-06", "currency": "GBP", "rate_to_eur": 0.86},
            ...
        ]
    """
    now = datetime.datetime.now()
    months = []
    for i in range(5):
        month = (now - datetime.timedelta(days=30 * i)).replace(day=1)
        months.append(month.strftime("%Y-%m"))

    fx_rates: list[dict[str, typing.Any]] = []
    for month in months:
        for currency in CURRENCIES:
            if currency == "EUR":
                rate = 1.0
            else:
                base = {
                    "CZK": 24.5,
                    "USD": 1.08,
                    "GBP": 0.86,
                    "JPY": 160.0,
                    "CAD": 1.45,
                    "AUD": 1.65,
                    "CHF": 0.97,
                    "SEK": 11.5,
                    "NOK": 11.7,
                }.get(currency, random.uniform(0.5, 30.0))
                rate = round(base * random.uniform(0.98, 1.02), 4)
            fx_rates.append({"month": month, "currency": currency, "rate_to_eur": rate})
    return fx_rates


def routine():
    """
    Generate mock data for Salesforce customers, BC global customers, and BC general ledger.
    Data is written to data/mock_data.json.
    """
    salesforce_payload: list[typing.Any] = []
    businesscentral_payload: list[typing.Any] = []

    sf_account_numbers: set[int] = set()
    for account_number in range(
        ACCOUNT_NUMBER_RANGE["min"], ACCOUNT_NUMBER_RANGE["max"]
    ):
        sf_payload = build_salesforce(account_number)
        salesforce_payload.append(sf_payload)
        sf_account_numbers.add(account_number)

    for account_number in range(
        ACCOUNT_NUMBER_RANGE["min"], ACCOUNT_NUMBER_RANGE["max"]
    ):
        bc_payload = build_businesscentral(account_number, sf_account_numbers)
        businesscentral_payload.append(bc_payload)

    accounts_payload = build_accounts_table()
    fx_rates_payload = build_fx_rates()
    journal_entries_payload = build_journal_entries(num_entries=500)

    ledger_payload = build_ledger(
        businesscentral_payload,
        journal_entries_payload,
        accounts_payload,
    )

    # Collect unique values for dimension tables from ledger
    entity_codes = sorted(
        {row["entity_code"] for row in ledger_payload if "entity_code" in row}
    )
    territories = sorted(
        {row["territory"] for row in ledger_payload if "territory" in row}
    )
    business_units = sorted(
        {row["business_unit"] for row in ledger_payload if "business_unit" in row}
    )
    consolidation_groups = sorted(
        {
            row["consolidation_group"]
            for row in ledger_payload
            if "consolidation_group" in row
        }
    )
    ix_codes = sorted(
        {row["ix_code"] for row in ledger_payload if "ix_code" in row}
    )

    # Build dimension tables with dummy metadata
    entity_codes_table = build_entity_codes_table(entity_codes)
    territories_table = build_territories_table(territories)
    business_units_table = build_business_units_table(business_units)
    consolidation_groups_table = build_consolidation_groups_table(consolidation_groups)
    ix_codes_table = build_ix_codes_table(ix_codes)

    output_dict: dict[str, typing.Any] = {
        "salesforce": {"customers": salesforce_payload},
        "business_central": {"global_customers": businesscentral_payload},
        "ledger": {"lines": ledger_payload},
        "fx_rates": {"rates": fx_rates_payload},
        "journal_entries": {"entries": journal_entries_payload},
        "accounts": {"dimension": accounts_payload},
        "entity_codes": entity_codes_table,
        "territories": territories_table,
        "business_units": business_units_table,
        "consolidation_groups": consolidation_groups_table,
        "ix_codes": ix_codes_table,
    }

    if not Path("data").exists():
        Path("data").mkdir()

    with open("data/mock_data.json", "w", encoding="utf-8") as file:
        json.dump(output_dict, file, indent=4)


if __name__ == "__main__":
    if Path("data/mock_data.json").exists():
        print(
            "Mock data already exists. Skipping... (delete 'data/mock_data.json' to regenerate)"
        )
    else:
        routine()
