import frappe
from frappe.model.document import Document

class ManufacturerItem(Document):

    def validate(self):
        self.validate_manufacturer_not_blocked()
        self.validate_unique_mapping()
        self.auto_fill_part_number()

    def validate_manufacturer_not_blocked(self):
        is_blocked = frappe.db.get_value(
            "Manufacturers",
            self.manufacturer,
            "is_blocked"
        )

        if is_blocked:
            frappe.throw(
                f"Manufacturers {self.manufacturer} is blocked. Cannot add items."
            )

    def validate_unique_mapping(self):
        exists = frappe.db.exists(
            "Manufacturer Item",
            {
                "manufacturer": self.manufacturer,
                "item_code": self.item_code,
                "name": ["!=", self.name]
            }
        )

        if exists:
            frappe.throw(
                "This Manufacturer–Item mapping already exists."
            )

    def auto_fill_part_number(self):
        if not self.part_number:
            self.part_number = self.item_code