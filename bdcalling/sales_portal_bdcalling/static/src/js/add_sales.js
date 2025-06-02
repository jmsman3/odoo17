/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import Dialog from "@web/legacy/js/core/dialog";

publicWidget.registry.CreateSales = publicWidget.Widget.extend({
    selector: "#add_sale, #update_sale",
    events: {
        'input .search-input': '_handleSearch',
        'click .search-option': '_onSearchOptionClick',
        "input #amount": "order_amount_cal",
        "change #sales_employee_id": "onSalesEmpChange",
        "change #percentage": "order_amount_cal",
        'input #delivery_last_date': 'updateRemainingTime',
        "click #btn_sbmt": "onSubmit",
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

        // Run once on load
        this.updateRemainingTime();

        // Start updating every second
        setInterval(() => {
            this.updateRemainingTime();
        }, 1000);
    },

    async _handleSearch(event) {
        const input = $(event.target);
        const model = input.data('model');
        const resultsContainer = input.siblings('.search-results');
        const searchTerm = input.val().trim();

        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }

        this.searchTimeout = setTimeout(async () => {
            if (searchTerm.length < 2) {
                resultsContainer.empty().hide();
                return;
            }
            try {
                const results = await this.rpc('/partner/search', {
                    model: model,
                    term: searchTerm
                });
                if (Array.isArray(results)) {
                    resultsContainer.empty();

                    if (results.length > 0) {
                        results.forEach(result => {
                            const option = $('<div>', {
                                class: 'search-option p-2 cursor-pointer hover:bg-gray-100',
                                'data-id': result.id,
                                text: result.name
                            });
                            console.log("Created option for result: ", result);
                            if (model === 'res.partner') {
                                option.data({
                                    'name': result.name,
                                    'email': result.email,
                                    'phone': result.phone,
                                });
                            } resultsContainer.append(option);
                        });
                        resultsContainer.show();
                    } else {
                        resultsContainer.html('<div class="p-2">No results found</div>').show();
                    }
                }
            } catch (error) {
                console.error('Search failed:', error);
                resultsContainer.html('<div class="p-2 text-danger">Error occurred while searching</div>').show();
            }
        }, 300);
    },


    async onSalesEmpChange(ev) {
        const employeeId = this.$("#sales_employee_id").val();
        if (!employeeId) return;
        try {
            const result = await this.rpc('/sale/get_sales_employee_info', { emp_id: employeeId });

            if (result.success) {
                this.$("#sales_company_name").val(result.company);
                this.$("#sales_employee_name").val(result.name);
                this.$("#sales_employee_id_hidden").val(result.employee_id);
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


    _onSearchOptionClick(event) {
        const option = $(event.currentTarget);
        const id = option.data('id');
        const name = option.text();
        const input = option.closest('.input-group').find('.search-input');
        const model = input.data('model');

        input.val(name).data('selected-id', id);
        option.closest('.search-results').hide();

        if (model === 'res.partner') {
            this.$("#partner_name").val(option.data('name') || '');
            this.$("#partner_email").val(option.data('email') || '');
            this.$("#partner_phone").val(option.data('phone') || '');

        }
    },
    updateRemainingTime() {
        var deliveryDateRaw = $("#delivery_last_date").val();

        if (!deliveryDateRaw) {
            $("#remaining_time").html(`<div class="text-muted">No delivery date set</div>`);
            return;
        }
        deliveryDateRaw = deliveryDateRaw.replace('T', ' ');
        var deliveryDate = new Date(`${deliveryDateRaw}:00`);

        if (isNaN(deliveryDate.getTime())) {
            $("#remaining_time").html(`<div class="text-muted">Invalid delivery date</div>`);
            return;
        }

        var currentDate = new Date();
        var timeDifference = deliveryDate.getTime() - currentDate.getTime();

        var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

        var remainingTime;
        if (timeDifference < 0) {
            remainingTime = `<div><span class="text-danger">Late delivery</span></div>`;
        } else {
            remainingTime = `<div> ${days}D | ${hours}H | ${minutes}M | ${seconds}S </div>`;
        }

        $("#remaining_time").html(remainingTime);
    },

    order_amount_cal() {
        console.log("order_amount_cal triggered");
        let amount = parseFloat($("#amount").val()) || 0;
        let percentage = parseInt($("#percentage").val()) || 0;
        let charges_amount = (percentage / 100) * amount;
        charges_amount = charges_amount.toFixed(2);
        let delivery_amount = amount - charges_amount;
        delivery_amount = delivery_amount.toFixed(2);

        console.log("amount: ", amount);
        console.log("percentage: ", percentage);
        console.log("charges_amount: ", charges_amount);
        console.log("delivery_amount: ", delivery_amount);

        $("#charges_amount").val(charges_amount);
        $("#delivery_amount").val(delivery_amount);
    },

    onPartnerChange(event) {
        console.log("Partner change event triggered");
        const selectedId = $(event.currentTarget).data('selected-id');
        const partner = this.getSelectedPartnerData(selectedId);

        // Set values in fields
        this.$("#partner_name").val(partner.name || "");
        this.$("#partner_email").val(partner.email || "");
        this.$("#partner_phone").val(partner.phone || "");


    },

    async getSelectedPartnerData(partnerId) {
        try {
            const result = await this.rpc('/rfq/get_partner', {
                partner_id: partnerId
            });
            return result;
        } catch (error) {
            console.error('Failed to fetch partner data:', error);
            return {};
        }
    },
    async onSubmit(ev) {
        ev.preventDefault();

        var missingFields = [];
        var $submitBtn = this.$el.find('button[type="submit"]');
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating Order...');
        // Extract remaining time text
        let remainingTimeText = this.$("#remaining_time").text().trim();
        let daysRemaining = 0;

        // Extract days if available
        let match = remainingTimeText.match(/(\d+)D/);
        if (match) {
            daysRemaining = parseInt(match[1], 10);
        }
        // var orderNumber = this.$("#order_number").val();
        // let platformSource = this.$("#platform_source_id").find(":selected").text().trim(); // Get the selected platform text
        // if (platformSource.toLowerCase() === "fiverr" && (!/^[A-Za-z0-9]{13}$/.test(orderNumber))) {
        //     missingFields.push("Order Number must be exactly 13 characters for Fiverr");
        // }
        if (!this.$('#partner_id').val()) {
            missingFields.push("Client Name");
        }
        if (!this.$('#product_id').val()) {
            missingFields.push("Service Type");
        }
        if (!this.$('#incoming_date').val()) {
            missingFields.push("Incoming Date");
        }

        if (!this.$('#amount').val()) {
            missingFields.push("Amount");
        }
        if (!this.$('#delivery_last_date').val()) {
            missingFields.push("Delivery Last Date");
        }


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
            employee_id: this.$("#employee_id").val(),
            sales_employee_id: this.$("#sales_employee_id_hidden").val(),
            partner_id: this.$("#partner_id").data('selected-id'),
            platform_source_id: this.$("#platform_source_id").val(),
            order_source_id: this.$("#order_source_id").val(),
            profile_id: this.$("#profile_id").val(),
            order_number: this.$("#order_number").val(),
            order_link: this.$("#order_link").val(),
            instruction_sheet_link: this.$("#instruction_sheet_link").val(),
            service_type_id: this.$("#product_id").val(),
            incoming_date: this.$("#incoming_date").val(),
            delivery_last_date: this.$("#delivery_last_date").val(),
            amount: this.$("#amount").val(),
            percentage: this.$("#percentage").val(),
            charges_amount: this.$("#charges_amount").val(),
            delivery_amount: this.$("#delivery_amount").val(),
            special_remarks: this.$("#special_remarks").val(),
            order_status: this.$("#order_status").val(),
            crm_tag_ids: this.$("#crm_tag_ids").val(),
            team_id: this.$("#team_id").val(),
            deadline: daysRemaining,
        };
        console.log("Form data--------------:", formData);

        try {
            const response = await this.rpc('/sale/create_quotation', formData);

            if (response.success) {
                new Dialog(this, {
                    title: "Success",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true, classes: 'btn-primary', click: function () { window.location.href = '/sale/dashboard'; } }],
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
        var order_id = this.$('#order_id').val();
        console.log('Book ID:', order_id);
        var missingFields = [];
        var $submitBtn = this.$el.find('button[type="submit"]');
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating Order...');
        // let orderNumber = this.$("#order_number").val();
        // let platformSource = this.$("#platform_source_id").find(":selected").text().trim();
        // if (platformSource.toLowerCase() === "fiverr" && (!/^[A-Za-z0-9]{13}$/.test(orderNumber))) {
        //     missingFields.push("Order Number must be exactly 13 characters for Fiverr");
        // }
        if (!this.$('#partner_id').val()) {
            missingFields.push("Client Name");
        }
        if (!this.$('#product_id').val()) {
            missingFields.push("Service Type");
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
            employee_id: this.$("#employee_id").val(),
            sales_employee_id: this.$("#sales_employee_id_hidden").val(),
            partner_id: this.$("#partner_id").data('selected-id'),
            platform_source_id: this.$("#platform_source_id").val(),
            order_source_id: this.$("#order_source_id").val(),
            profile_id: this.$("#profile_id").val(),
            order_number: this.$("#order_number").val(),
            order_link: this.$("#order_link").val(),
            instruction_sheet_link: this.$("#instruction_sheet_link").val(),
            service_type_id: this.$("#product_id").val(),
            incoming_date: this.$("#incoming_date").val(),
            delivery_last_date: this.$("#delivery_last_date").val(),
            amount: this.$("#amount").val(),
            percentage: this.$("#percentage").val(),
            charges_amount: this.$("#charges_amount").val(),
            delivery_amount: this.$("#delivery_amount").val(),
            special_remarks: this.$("#special_remarks").val(),
            order_status: this.$("#order_status").val(),
            crm_tag_ids: this.$("#crm_tag_ids").val(),
            order_id: order_id,
            team_id: this.$("#team_id").val(),
        };
        console.log("Form data--------------:", formData);
        try {
            const response = await this.rpc('/sale/update', formData);
            console.log("Server Response:", response);

            if (response.success) {
                new Dialog(this, {
                    title: "Success",
                    size: 'medium',
                    buttons: [{ text: 'Ok', close: true, classes: 'btn-primary', click: function () { window.location.href = '/sale/dashboard'; } }],
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
            console.error("Error:", error);
            new Dialog(this, {
                title: "Error",
                size: 'medium',
                buttons: [{ text: 'Ok', close: true, classes: 'btn-primary' }],
                $content: $('<p/>', { text: "An error occurred while saving the data. See console for details." }),
            }).open();
        } finally {
            $submitBtn.prop('disabled', false).text('Submit');
        }
    },
});