frappe.ui.form.on("Employee Tax Exemption Declaration", {

    setup(frm) {
        frm.trigger("set_description_amount_from_exemption_rule");
    },

    set_description_amount_from_exemption_rule(frm) {
        // Find token {{amount}} in description and replace with value from exemption rule
        frappe.call({
            method: "thai_payroll.custom.employee_tax_exemption_declaration.get_income_tax_exemption_rule",
            args: {
                payroll_period: frm.doc.payroll_period,
            },
            callback: function(r) {
                // List of fields to set description [doc_field, rule_field]
                console.log(r)
                const amount_fields = [
                    ["custom_elderly_exemption", "elderly_exemption"],
                    ["custom_elderly_spouse_exemption", "elderly_spouse_exemption"],
                    ["custom_disable_person_exemption", "disable_person_exemption"],
                    ["custom_compensation_by_labor_law", "compensation_by_labor_law"],
                    ["custom_exemption", "exemption"],
                    ["custom_spouse_exemption", "spouse_exemption"],
                    ["custom_child_born_before_2561", "child_born_before_2561"],
                    ["custom_child_born_from_2561", "child_born_from_2561"],
                    ["custom_own_father_exemption", "own_father_exemption"],
                    ["custom_own_mother_exemption", "own_mother_exemption"],
                    ["custom_spouse_father_exemption", "spouse_father_exemption"],
                    ["custom_spouse_mother_exemption", "spouse_mother_exemption"],
                    ["custom_disable_person_support", "disable_person_support"],
                    ["custom_invest_in_annuity", "invest_in_annuity"],
                    ["custom_pension_life_insurance", "pension_life_insurance"],
                    ["custom_total_contribution", "total_contribution"],
                    ["custom_social_security", "social_security"],
                    ["custom_maternity_expense", "maternity_expense"],
                    ["custom_life_insurance", "life_insurance"],
                    ["custom_spouse_life_insurance", "spouse_life_insurance"],
                    ["custom_health_insurance", "health_insurance"],
                    ["custom_health_insurance_for_parents", "health_insurance_for_parents"],
                    ["custom_invest_in_thai_esg", "invest_in_thai_esg"],
                    ["custom_interest_paid_for_housing_loan", "interest_paid_for_housing_loan"],
                    ["custom_donation_for_political_party", "donation_for_political_party"],
                    ["custom_expense", "expense"]
                ];
                const regex = /\{\{\s*amount\s*\}\}/;
                amount_fields.forEach(amount_field => {
                    let field = frm.get_docfield(amount_field[0]);
                    if (regex.test(field.description)) {
                        let amount = new Intl.NumberFormat("en-US").format(r.message[amount_field[1]]);
                        const updatedDescription = field.description.replace(regex, amount);
                        frm.set_df_property(amount_field[0], "description", updatedDescription);
                    }
                });
            }
        });
    },

    custom_get_yearly_salary: function(frm) {
		frappe.call({
			method: "thai_payroll.custom.employee_tax_exemption_declaration.get_employee_yearly_salary",
			args: {
				company: frm.doc.company,
				payroll_period: frm.doc.payroll_period,
				employee: frm.doc.employee,
				is_opening_entry: frm.doc.custom_is_opening_entry,
				opening_entry_date: frm.doc.custom_opening_entry_date
			},
			callback: function (r) {
				frm.set_value("custom_yearly_salary", r.message);
				frm.set_value("custom_yearly_bonus", 0);
			},
		});
	},

	custom_get_yearly_pvd_contribution: function(frm) {
		frappe.call({
			method: "thai_payroll.custom.employee_tax_exemption_declaration.get_employee_yearly_pvd_contribution",
			args: {
				company: frm.doc.company,
				payroll_period: frm.doc.payroll_period,
				employee: frm.doc.employee,
				is_opening_entry: frm.doc.custom_is_opening_entry,
				opening_entry_date: frm.doc.custom_opening_entry_date
			},
			callback: function (r) {
				frm.set_value("custom_pvd_contribution", r.message);
			},
		});
	},

})
