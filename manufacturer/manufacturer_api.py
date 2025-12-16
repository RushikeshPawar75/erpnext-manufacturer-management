import frappe
from frappe import _


@frappe.whitelist()
def create_item_with_manufacturer(payload=None):
    if not payload:
        payload = frappe.form_dict

    if isinstance(payload, str):
        payload = frappe.parse_json(payload)

    if not isinstance(payload, dict):
        frappe.throw(_("Invalid payload format"))
    for key in ["item_code", "item_name", "item_group", "stock_uom"]:
        if not payload.get(key):
            frappe.throw(_(f"Missing field: {key}"))

    manufacturer_data = payload.get("manufacturers")
    if not manufacturer_data:
        frappe.throw(_("Manufacturers block is required"))

    manufacturer_name = manufacturer_data.get("manufacturer_name")
    if not manufacturer_name:
        frappe.throw(_("manufacturer_name is required"))

    if not frappe.db.exists("Item Group", payload["item_group"]):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": payload["item_group"],
            "parent_item_group": "All Item Groups"
        }).insert(ignore_permissions=True)

    if not frappe.db.exists("Item", payload["item_code"]):
        frappe.get_doc({
            "doctype": "Item",
            "item_code": payload["item_code"],
            "item_name": payload["item_name"],
            "item_group": payload["item_group"],
            "stock_uom": payload["stock_uom"],
            "is_stock_item": 1
        }).insert(ignore_permissions=True)


    if not frappe.db.exists("Manufacturers", manufacturer_name):
        frappe.get_doc({
            "doctype": "Manufacturers",
            "manufacturer_name": manufacturer_name,
            "gln": manufacturer_data.get("gln"),
            "is_blocked": manufacturer_data.get("is_blocked", 0)
        }).insert(ignore_permissions=True)

    manufacturer = frappe.get_doc("Manufacturers", manufacturer_name)

    if manufacturer.is_blocked:
        frappe.throw(_(f"Manufacturer {manufacturer_name} is blocked"))

    if not frappe.db.exists(
        "Manufacturer Item",
        {
            "manufacturer": manufacturer.name,
            "item_code": payload["item_code"]
        }
    ):
        frappe.get_doc({
            "doctype": "Manufacturer Item",
            "manufacturer": manufacturer.name,
            "item_code": payload["item_code"],
            "part_number": payload["item_code"],
            "gtin": manufacturer_data.get("gtin")
        }).insert(ignore_permissions=True)

    frappe.db.commit()

    return {
        "status": "success",
        "item": payload["item_code"],
        "manufacturer": manufacturer.name
    }
