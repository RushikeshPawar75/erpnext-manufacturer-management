frappe.query_reports["Items by Manufacturer"] = {
    filters: [
        {
            fieldname: "manufacturer",
            label: __("Manufacturer"),
            fieldtype: "Link",
            options: "Manufacturers",
            get_query: function () {
                return {
                    filters: {
                        is_blocked: 0
                    }
                };
            }
        },
        {
            fieldname: "item_code",
            label: __("Item"),
            fieldtype: "Link",
            options: "Item",
            get_query: function () {
                const manufacturer =
                    frappe.query_report.get_filter_value("manufacturer");

                if (!manufacturer) {
                    return {};
                }

                return {
                    query:
                        "manufacturer.manufacturer.report.items_by_manufacturer.items_by_manufacturer.get_items_by_manufacturer",
                    filters: {
                        manufacturer: manufacturer
                    }
                };
            }
        }
    ]
};


frappe.query_report.onload = function () {
    frappe.query_report.get_filter("manufacturer").df.onchange = function () {
        frappe.query_report.set_filter_value("item_code", null);
    };
};
