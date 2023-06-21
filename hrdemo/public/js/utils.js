frappe.provide("hrdemo");
frappe.provide("hrdemo.utils");

$.extend(hrdemo, {
	proceed_save_with_reminders_frequency_change: () => {
		frappe.ui.hide_open_dialog();
		frappe.call({
			method: 'hrdemo.hr.doctype.hr_settings.hr_settings.set_proceed_with_frequency_change',
			callback: () => {
				cur_frm.save();
			}
		});
	}
})