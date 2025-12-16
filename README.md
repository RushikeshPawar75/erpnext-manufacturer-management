### Manufacturer

Manufacturer

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app manufacturer
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/manufacturer
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit


MODULE 2: MANUFACTURERS – ITEM MAPPING
=================================

Overview
--------
The Manufacturers–Item Mapping module links manufacturers to stock items using
part numbers and GTINs while enforcing data integrity rules.

Target Platform: ERPNext v15+ / Frappe Framework


FEATURES
--------

1. DocTypes

Manufacturers
- manufacturer_name (Data, Unique)
- gln (Data)
- is_blocked (Check)

Manufacturer Item
- manufacturer (Link → Manufacturers)
- item_code (Link → Item)
- part_number (Data)
- gtin (Data)


2. Business Validations

- Block creation if Manufacturer is marked as blocked
- Enforce unique (manufacturer, item_code) mapping
- Auto-fill part_number with item_code if empty

Implemented in ManufacturerItem.validate()


3. Client Script

- Automatically sets part_number = item_code when item_code is selected


4. REST API – Create Item with Manufacturer

Endpoint:
POST /api/method/manufacturer.api.create_item_with_manufacturer

Behavior:
- Creates Item Group if missing
- Creates Item if missing
- Creates Manufacturer if missing
- Creates Manufacturer Item mapping
- Prevents mapping if Manufacturer is blocked

Sample Payload:
{
  "item_code": "IBUPROFEN-500-CIP",
  "item_name": "Ibuprofen 500mg Tablet - Cipla",
  "item_group": "Pharmacy Items",
  "stock_uom": "Nos",
  "manufacturers": {
    "manufacturer_name": "Cipla Ltd",
    "gln": "8901234500001",
    "gtin": "08901234567891",
    "is_blocked": 0
  }
}


5. Report – Items by Manufacturer

Filters:
- Manufacturer (only non-blocked)
- Item (filtered dynamically)

Columns:
- Manufacturer
- Item Code
- Item Name
- Part Number
- GTIN

Report Type:
- Script Report (SQL-based)


FIXTURES / SAMPLE DATA
---------------------
- 2 Manufacturers
- 3 Items
- 4 Manufacturer–Item mappings


AI USAGE LOG (SUMMARY)
---------------------
Issue: Enforce unique manufacturer–item mapping
Prompt: How to enforce unique combination in ERPNext?
AI Suggested: Use frappe.db.exists in validate()
Implemented: Custom validation

Issue: Block creation if parent is blocked
Prompt: How to restrict child creation based on parent flag?
AI Suggested: Validate parent field in validate()
Implemented: Manufacturer blocked check


SETUP
-----
bench get-app manufacturer
bench --site yoursite.local install-app manufacturer
bench migrate
