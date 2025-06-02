/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import Dialog from "@web/legacy/js/core/dialog";

publicWidget.registry.CreateOperation = publicWidget.Widget.extend({
    selector: "#add_operation,#update_operation",
    events: {
        "click #btn_sbmt": "onSubmit",
        "change #order_id": "onOrderChange",
        "change #employee_id": "onEmpChange",
        "input #delivery_amount": "order_amount_cal",
        "change #percentage": "order_amount_cal",
        "click #btn_update": "onUpdate",
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
        this.searchTimeout = null;

    },
    start() {
        console.log("started js__________________");
        this._super(...arguments);

    },

    order_amount_cal() {
        console.log("order_amount_cal triggered");

        let delivery_amount = parseFloat($("#delivery_amount").val()) || 0;
        let percentage = parseInt($("#percentage").val()) || 0;

        let charges_amount = (percentage / 100) * delivery_amount;
        charges_amount = charges_amount.toFixed(2);

        let monetary_value = delivery_amount - charges_amount;
        monetary_value = monetary_value.toFixed(2);

        console.log("percentage: ", percentage);
        console.log("charges_amount: ", charges_amount);
        console.log("monetary_value: ", monetary_value);

        $("#monetary_value").val(monetary_value);
    },


    async onOrderChange(ev) {
        const orderNumber = this.$("#order_id").val();
        if (!orderNumber) return;

        try {
            const result = await this.rpc('/sale/get_order_info', { order_number: orderNumber });

            if (result.success) {
                // Fill form fields with fetched data
                this.$("#so_id").val(result.so_id);
                this.$("#delivery_amount").val(result.delivery_amount);
                this.$("#instruction_sheet_link").val(result.instruction_sheet_link);
                this.$("#team_id").val(result.team_id);
                this.$("#partner_id").val(result.partner_name);
                this.$("#order_link").val(result.order_link);
                // console.log("partner id:", result.partner_id.name)
                console.log("Order Data Loaded:", result);
            } else {
                new Dialog(this, {
                    title: "Error",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true }],
                    $content: $('<p/>', { text: result.message }),
                }).open();
            }
        } catch (error) {
            console.error("Error fetching order data:", error);
            new Dialog(this, {
                title: "Error",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true }],
                $content: $('<p/>', { text: result.message }),
            }).open();
        }
    },



    async onEmpChange(ev) {
        const employeeId = this.$("#employee_id").val();
        if (!employeeId) return;

        try {
            const result = await this.rpc('/sale/get_sales_employee_info', { emp_id: employeeId });

            if (result.success) {
                this.$("#employee_name").val(result.company);
                this.$("#company_name").val(result.name);
                this.$("#employee_id_hidden").val(result.employee_id); 
                console.log("Employee Data Loaded:", result);
            } else {
                new Dialog(this, {
                    title: "Error",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true }],
                    $content: $('<p/>', { text: result.message }),
                }).open();
            }
        } catch (error) {
            console.error("Error fetching order data:", error);
            new Dialog(this, {
                title: "Error",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true }],
                $content: $('<p/>', { text: result.message }),
            }).open();
        }
    },




    async onSubmit(ev) {
        ev.preventDefault();

        var missingFields = [];
        var $submitBtn = this.$el.find('button[type="submit"]');
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating Order...');

        if (!this.$('#order_id').val()) {
            missingFields.push("Order ID");
        }
        if (!this.$('#date').val()) {
            missingFields.push("Date");
        }

        if (!this.$('#delivery_amount').val()) {
            missingFields.push("Delivery Amount");
        }
        // If there are missing required fields, show a dialog
        if (missingFields.length > 0) {
            new Dialog(this, {
                title: "Required Fields Missing",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true, classes: 'btn-primary' }],
                $content: $('<p/>', { text: "Please fill in the following required fields: " + missingFields.join(', ') }),
            }).open();
            $submitBtn.prop('disabled', false).text('Submit');

            return;
        }
        const formData = {
            employee_id: this.$("#employee_id_hidden").val(),
            date: this.$("#date").data('selected-id'),
            order_id: this.$("#order_id").val(),
            so_id: this.$("#so_id").val(),
            instruction_sheet_link: this.$("#instruction_sheet_link").val(),
            percentage: this.$("#percentage").val(),
            monetary_value: this.$("#monetary_value").val(),
            delivery_amount: this.$("#delivery_amount").val(),
            special_remarks: this.$("#special_remarks").val(),
            order_status: this.$("#order_status").val(),
            order_link: this.$("#order_link").val(),
            partner_id: this.$("#partner_id").val(),
            team_id: this.$("#team_id").val(),
            project: this.$("#project").val(),
        };
        console.log("Form data--------------:", formData);

        try {
            const response = await this.rpc('/sale/create_operation', formData);

            if (response.success) {
                new Dialog(this, {
                    title: "Success",
                    size: 'medium',
                    buttons: [
                        {
                            text: 'Ok',
                            close: true,
                            classes: 'btn-primary',
                            click: function () {
                                window.location.href = '/sale/operation';
                            },
                        }
                    ],
                    $content: $(`
                        <div class="text-center p-3">
                            <div class="mb-3">
                                <i class="fas fa-check-circle" style="font-size: 48px; color: #28a745;"></i>
                            </div>
                            <h4 class="text-success mb-2">Success!</h4>
                            <p class="text-muted">${response.message}</p>
                        </div>
                    `),
                }).open();
            } else {
                new Dialog(this, {
                    title: "Error",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true }],
                    $content: $('<p/>', { text: response.message || response.error || "An unknown error occurred." }),
                }).open();
            }
        } catch (error) {
            console.error("Error:", error);
            new Dialog(this, {
                title: "Error",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true, classes: 'btn-primary' }],
                $content: $('<p/>', { text: "An error occurred while saving the data." }),
            }).open();
        } finally {
            // Remove loading state
            $submitBtn.prop('disabled', false).text('Submit');
        }
    },

    async onUpdate(ev) {
        ev.preventDefault();

        var missingFields = [];
        var $submitBtn = this.$el.find('button[type="submit"]');
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Updating Order...');

        if (!this.$('#order_id').val()) {
            missingFields.push("Order ID");
        }
        if (!this.$('#date').val()) {
            missingFields.push("Date");
        }
        if (!this.$('#delivery_amount').val()) {
            missingFields.push("Delivery Amount");
        }
        // If there are missing required fields, show a dialog
        if (missingFields.length > 0) {
            new Dialog(this, {
                title: "Required Fields Missing",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true, classes: 'btn-primary' }],
                $content: $('<p/>', { text: "Please fill in the following required fields: " + missingFields.join(', ') }),
            }).open();
            $submitBtn.prop('disabled', false).text('Submit');

            return;
        }
        const formData = {
            employee_id: this.$("#employee_id_hidden").val(),
            date: this.$("#date").val(),
            order_id: this.$("#order_id").val(),
            so_id: this.$("#so_id").val(),
            instruction_sheet_link: this.$("#instruction_sheet_link").val(),
            percentage: this.$("#percentage").val(),
            monetary_value: this.$("#monetary_value").val(),
            delivery_amount: this.$("#delivery_amount").val(),
            special_remarks: this.$("#special_remarks").val(),
            order_status: this.$("#order_status").val(),
            order_link: this.$("#order_link").val(),
            partner_id: this.$("#partner_id").val(),
            team_id: this.$("#team_id").val(),
            project: this.$("#project").val(),
            revision_count: this.$("#revision_count").val(),
        };
        console.log("Form data--------------:", formData);

        try {
            const response = await this.rpc('/operation/update', formData);
            console.log("Server Response:", response);
            if (response.success) {
                new Dialog(this, {
                    title: "Success",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true, classes: 'btn-primary', click: function () { window.location.href = '/operation_dashboard'; } }],
                    $content: $(`
                        <div class="text-center p-3">
                            <div class="mb-3">
                                <i class="fas fa-check-circle" style="font-size: 48px; color: #28a745;"></i>
                            </div>
                            <h4 class="text-success mb-2">Success!</h4>
                            <p class="text-muted">${response.message}</p>
                        </div>
                    `),
                }).open();
            } else {
                console.error("Error response from server:", response);
                new Dialog(this, {
                    title: "Error",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true }],
                    $content: $('<p/>', { text: response.message || "Unknown error occurred." }),
                }).open();
            }
        } catch (error) {
            new Dialog(this, {
                title: "Error",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true, classes: 'btn-primary' }],
                $content: $('<p/>', { text: "An error occurred while saving the data. See console for details." }),
            }).open();
        } finally {
            // Remove loading state
            $submitBtn.prop('disabled', false).text('Submit');
        }  
    },
});