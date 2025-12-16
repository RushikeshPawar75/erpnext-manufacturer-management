frappe.ui.form.on("Manufacturer Item", {
    item_code(frm) {
        if (!frm.doc.part_number && frm.doc.item_code) {
            frm.set_value("part_number", frm.doc.item_code);
        }
    }
});