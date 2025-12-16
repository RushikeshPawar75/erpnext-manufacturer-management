import frappe


def execute(filters=None):
    filters = filters or {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": "Manufacturer",
            "fieldname": "manufacturer",
            "fieldtype": "Link",
            "options": "Manufacturer",
            "width": 200
        },
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 180
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "width": 250
        },
        {
            "label": "Part Number",
            "fieldname": "part_number",
            "width": 150
        },
        {
            "label": "GTIN",
            "fieldname": "gtin",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("manufacturer"):
        conditions += " AND mi.manufacturer = %(manufacturer)s"
        values["manufacturer"] = filters["manufacturer"]

    if filters.get("item_code"):
        conditions += " AND mi.item_code = %(item_code)s"
        values["item_code"] = filters["item_code"]

    query = f"""
        SELECT
            mi.manufacturer,
            mi.item_code,
            i.item_name,
            mi.part_number,
            mi.gtin
        FROM `tabManufacturer Item` mi
        INNER JOIN `tabItem` i ON i.name = mi.item_code
        WHERE 1=1 {conditions}
        ORDER BY mi.manufacturer, mi.item_code
    """

    return frappe.db.sql(query, values, as_dict=True)




@frappe.whitelist()
def get_items_by_manufacturer(doctype, txt, searchfield, start, page_len, filters):
    manufacturer = filters.get("manufacturer")

    if not manufacturer:
        return []

    return frappe.db.sql("""
        SELECT DISTINCT
            mi.item_code, mi.item_code
        FROM `tabManufacturer Item` mi
        INNER JOIN `tabManufacturers` m
            ON m.name = mi.manufacturer
        WHERE
            mi.manufacturer = %(manufacturer)s
            AND m.is_blocked = 0
            AND mi.item_code LIKE %(txt)s
        ORDER BY mi.item_code
        LIMIT %(start)s, %(page_len)s
    """, {
        "manufacturer": manufacturer,
        "txt": f"%{txt}%",
        "start": start,
        "page_len": page_len
    })

