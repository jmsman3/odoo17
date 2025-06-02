/** @odoo-module **/

import Dialog from "@web/legacy/js/core/dialog";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CreateCustomer = publicWidget.Widget.extend({
    selector: "#create_customer",
    events: {
        // 'input .search-input': '_handleSearch',
        // 'click .search-option': '_onSearchOptionClick',
        "click #btn_sbmt": "onSubmit",
        "click #uploadImageBtn": "onImageUpload",
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
        this.searchTimeout = null;

    },
    start() {
        console.log("started js__________________");
        return this._super(...arguments);
    },

    async onSubmit(ev) {
        ev.preventDefault();
        var missingFields = [];
        var $submitBtn = this.$el.find("#btn_sbmt");
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...');

        if (!this.$("#partner_id").val()) {
            missingFields.push("Please select a customer");
        }
        // Validate email
        // const email = this.$("#partner_email").val();
        // if (email) {
        //     if (!/^.+@.+\..+$/.test(email)) {
        //         missingFields.push("Invalid email address");
        //     }
        // }

        // // Validate phone
        // const phone = this.$("#partner_phone").val();
        // if (phone) { 
        //     if (!/^\+?\d{10,14}$/.test(phone)) {
        //         missingFields.push("Invalid phone number");
        //     }
        // }

        // let imageBase64 = null;
        // const fileInput = this.$("#image_1920")[0];
        // if (fileInput.files.length > 0) {
        //     const file = fileInput.files[0];
        //     imageBase64 = await this._convertImageToBase64(file);
        // }

        // if (missingFields.length > 0) {
        //     alert(missingFields.join("\n"));
        //     $submitBtn.prop("disabled", false).text("Submit");
        //     return;
        // }



        // Collect form data
        const formData = {
            partner_id: this.$("#partner_id").data('selected-id'),
            partner_name: this.$("#partner_name").val(),
            // partner_email: this.$("#partner_email").val(),
            // partner_phone: this.$("#partner_phone").val(),
            // partner_address: this.$("#partner_address").val(),
            // partner_city: this.$("#partner_city").val(),
            // partner_state: this.$("#partner_state").val(),
            partner_country: this.$("#partner_country").val(),
            partner_zip: this.$("#partner_zip").val(),
            // partner_website: this.$("#partner_website").val(),
            // image_1920: imageBase64,
        };
        console.log("Form Data: ", formData);

        try {
            const response = await this.rpc("/customer/submit", formData);
            if (response.success) {
                new Dialog(this, {
                    title: "",
                    size: "medium",
                    buttons: [{
                        text: "Go Back",
                        classes: "btn btn-success",
                        close: true,
                        click: () => window.history.back()
                    }],
                    $content: $(`
                        <div class="text-center p-4">
                            <i class="fa fa-check-circle" style="font-size: 48px; color: #28a745;"></i>
                            <h4 class="mt-3 text-success">Success!</h4>
                            <p class="mt-2"><b>${response.message || "Your action was successful."}</b></p>
                        </div>
                    `),
                }).open();
            }
             else {
                new Dialog(this, {
                    title: "Error",
                    size: "medium",
                    buttons: [{ text: "Ok", close: true }],
                    $content: $("<p/>", { text: response.error || "Unknown error" }),
                }).open();
            }
        } catch (error) {
            console.error("Error:", error);
            new Dialog(this, {
                title: "Error",
                size: "medium",
                buttons: [{ text: "Ok", close: true }],
                $content: $("<p/>", { text: "An error occurred while saving the data." }),
            }).open();
        } finally {
            $submitBtn.prop("disabled", false).text("Submit");
        }
    },

    _convertImageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result.split(",")[1]);
            reader.onerror = (e) => reject(e);
            reader.readAsDataURL(file);
        });
    },
});


//Rayta apu codes

// /** @odoo-module **/

// import Dialog from "@web/legacy/js/core/dialog";
// import publicWidget from "@web/legacy/js/public/public_widget";

// publicWidget.registry.CreateCustomer = publicWidget.Widget.extend({
//     selector: "#create_customer",
//     events: {
//         // 'input .search-input': '_handleSearch',
//         // 'click .search-option': '_onSearchOptionClick',
//         "click #btn_sbmt": "onSubmit",
//         "click #uploadImageBtn": "onImageUpload",
//     },

//     init() {
//         this._super(...arguments);
//         this.rpc = this.bindService("rpc");
//         this.searchTimeout = null;

//     },
//     start() {
//         console.log("started js__________________");
//         return this._super(...arguments);
//     },

//     async onSubmit(ev) {
//         ev.preventDefault();
//         var missingFields = [];
//         var $submitBtn = this.$el.find("#btn_sbmt");
//         $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...');

//         if (!this.$("#partner_id").val()) {
//             missingFields.push("Please select a customer");
//         }
//         // // Validate email
//         // const email = this.$("#partner_email").val();
//         // if (email) {
//         //     if (!/^.+@.+\..+$/.test(email)) {
//         //         missingFields.push("Invalid email address");
//         //     }
//         // }

//         // // Validate phone
//         // const phone = this.$("#partner_phone").val();
//         // if (phone) { 
//         //     if (!/^\+?\d{10,14}$/.test(phone)) {
//         //         missingFields.push("Invalid phone number");
//         //     }
//         // }

//         // let imageBase64 = null;
//         // const fileInput = this.$("#image_1920")[0];
//         // if (fileInput.files.length > 0) {
//         //     const file = fileInput.files[0];
//         //     imageBase64 = await this._convertImageToBase64(file);
//         // }

//         if (missingFields.length > 0) {
//             alert(missingFields.join("\n"));
//             $submitBtn.prop("disabled", false).text("Submit");
//             return;
//         }



//         // Collect form data
//         const formData = {
//             partner_id: this.$("#partner_id").data('selected-id'),
//             partner_name: this.$("#partner_name").val(),
//             // partner_email: this.$("#partner_email").val(),
//             // partner_phone: this.$("#partner_phone").val(),
//             // partner_address: this.$("#partner_address").val(),
//             // partner_city: this.$("#partner_city").val(),
//             // partner_state: this.$("#partner_state").val(),
//             partner_country: this.$("#partner_country").val(),
//             partner_zip: this.$("#partner_zip").val(),
//             // partner_website: this.$("#partner_website").val(),
//             // image_1920: imageBase64,
//         };
//         console.log("Form Data: ", formData);

//         try {
//             const response = await this.rpc("/customer/submit", formData);
//             if (response.success) {
//                 new Dialog(this, {
//                     title: "",
//                     size: "medium",
//                     buttons: [{
//                         text: "Go Back",
//                         classes: "btn btn-success",
//                         close: true,
//                         click: () => window.history.back()
//                     }],
//                     $content: $(`
//                         <div class="text-center p-4">
//                             <i class="fa fa-check-circle" style="font-size: 48px; color: #28a745;"></i>
//                             <h4 class="mt-3 text-success">Success!</h4>
//                             <p class="mt-2"><b>${response.message || "Your action was successful."}</b></p>
//                         </div>
//                     `),
//                 }).open();
//             }
//              else {
//                 new Dialog(this, {
//                     title: "Error",
//                     size: "medium",
//                     buttons: [{ text: "Ok", close: true }],
//                     $content: $("<p/>", { text: response.error || "Unknown error" }),
//                 }).open();
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             new Dialog(this, {
//                 title: "Error",
//                 size: "medium",
//                 buttons: [{ text: "Ok", close: true }],
//                 $content: $("<p/>", { text: "An error occurred while saving the data." }),
//             }).open();
//         } finally {
//             $submitBtn.prop("disabled", false).text("Submit");
//         }
//     },

//     _convertImageToBase64(file) {
//         return new Promise((resolve, reject) => {
//             const reader = new FileReader();
//             reader.onload = (e) => resolve(e.target.result.split(",")[1]);
//             reader.onerror = (e) => reject(e);
//             reader.readAsDataURL(file);
//         });
//     },
// });






//old codes
    // async _handleSearch(event) {
    //     const input = $(event.target);
    //     const model = input.data('model');
    //     const resultsContainer = input.siblings('.search-results');
    //     const searchTerm = input.val().trim();
        
    //     if (this.searchTimeout) {
    //         clearTimeout(this.searchTimeout);
    //     }
    
    //     this.searchTimeout = setTimeout(async () => {
    //         if (searchTerm.length < 2) {
    //             resultsContainer.empty().hide();
    //             return;
    //         }
    
    //         try {
    //             const results = await this.rpc('/partner/search', {
    //                 model: model,
    //                 term: searchTerm
    //             });
    //             if (Array.isArray(results)) {
    //                 resultsContainer.empty();
                    
    //                 if (results.length > 0) {
    //                     results.forEach(result => {
    //                         const option = $('<div>', {
    //                             class: 'search-option p-2 cursor-pointer hover:bg-gray-100',
    //                             'data-id': result.id,
    //                             text: result.name
    //                         });
    //                         console.log("Created option for result: ", result);
    //                         if (model === 'res.partner') {
    //                             option.data({
    //                                 'name': result.name,
    //                                 'email': result.email,
    //                                 'phone': result.phone,
    //                                 'street': result.street,
    //                                 'city': result.city,
    //                                 'state': result.state,
    //                                 'country': result.country,
    //                                 'zip': result.zip,
    //                                 'website': result.website,
    //                             });
    //                         }resultsContainer.append(option);
    //                     });
    //                     resultsContainer.show();
    //                 } else {
    //                     resultsContainer.html('<div class="p-2">No results found</div>').show();
    //                 }
    //             }
    //         } catch (error) {
    //             console.error('Search failed:', error);
    //             resultsContainer.html('<div class="p-2 text-danger">Error occurred while searching</div>').show();
    //         }
    //     }, 300);
    // },
    
    // _onSearchOptionClick(event) {
    //     const option = $(event.currentTarget);
    //     const id = option.data('id');
    //     const name = option.text();
    //     const input = option.closest('.input-group').find('.search-input');
    //     const model = input.data('model');
        
    //     input.val(name).data('selected-id', id);
    //     option.closest('.search-results').hide();

    //     if (model === 'res.partner') {
    //         this.$("#partner_name").val(option.data('name') || '');
    //         this.$("#partner_email").val(option.data('email') || '');
    //         this.$("#partner_phone").val(option.data('phone') || '');
    //         this.$("#partner_address").val(option.data('street') || '');
    //         this.$("#partner_city").val(option.data('city') || '');
    //         this.$("#partner_state").val(option.data('state') || '');
    //         this.$("#partner_country").val(option.data('country') || '');
    //         this.$("#partner_zip").val(option.data('zip') || '');
    //         this.$("#partner_website").val(option.data('website') || '');
            
    //     }
    // },

    // onPartnerChange(event) {    
    //     console.log("Partner change event triggered");
    //     const selectedId = $(event.currentTarget).data('selected-id');
    //     const partner = this.getSelectedPartnerData(selectedId);
    
    //     // Set values in fields
    //     this.$("#partner_name").val(partner.name || "");
    //     this.$("#partner_email").val(partner.email || "");
    //     this.$("#partner_phone").val(partner.phone || "");
    //     this.$("#partner_address").val(partner.street || "");
    //     this.$("#partner_city").val(partner.city || "");
    //     this.$("#partner_state").val(partner.state || "");
    //     this.$("#partner_country").val(partner.country || "");
    //     this.$("#partner_zip").val(partner.zip || "");
    //     this.$("#partner_website").val(partner.website || "");

    // },
    
    // async getSelectedPartnerData(partnerId) {
    //     try {
    //         const result = await this.rpc('/rfq/get_partner', {
    //             partner_id: partnerId
    //         });
    //         return result;
    //     } catch (error) {
    //         console.error('Failed to fetch partner data:', error);
    //         return {};
    //     }
    // },
    