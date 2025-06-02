/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ProductRequisition = publicWidget.Widget.extend({
    selector: "#requisition",
    events: {
        "change #req_att_files": "_onRequestFileChange",
        "change #req_ap_att_files": "_onApprovalFileChange",
        "click #p_line_add_product": "_onAddProductLine",
        "click .remove_product_line": "_onRemoveProductLine",
        "keyup .line_item": "_onLineItemChange",
        "focusin .search": "_onSearchFocus",
        "keyup .search": "_onSearchKeyup",
        "click .sugg_product": "_onSelectSuggestedProduct",
        "change .search": "_onProductChange",
        "change .product_line_file": "_onProductLineFileChange",
        "click .attach_file_btn": "_onAttachFileClick",
        "submit": "_onFormSubmit",
    },

    init() {
        this._super(...arguments);
        this.product_lines = [];
        this.product_line_id = 1;
        this.sel_line_id = null;
        this.searchTimeout = null;
    },

    start() {
        this._super(...arguments);
        // Hide all suggestion dropdowns initially
        $(".query_sugg").hide();

        // Add click handler to document to close dropdowns when clicking outside
        $(document).click((event) => {
            if (!$(event.target).hasClass('search')) {
                $('.query_sugg').hide();
            }
        });
    },

    _onRequestFileChange(ev) {
        const files = ev.target.files;
        let html = '';
        for (let i = 0; i < files.length; i++) {
            html += `<li class="list-group-item">
                <i class="fa fa-file me-2"></i>${files[i].name}
            </li>`;
        }
        $("#con_req_att_list").show();
        $("#req_att_list").html(html);
    },

    _onApprovalFileChange(ev) {
        const files = ev.target.files;
        let html = '';
        for (let i = 0; i < files.length; i++) {
            html += `<li class="list-group-item">
                <i class="fa fa-file me-2"></i>${files[i].name}
            </li>`;
        }
        $("#con_req_ap_att_list").show();
        $("#req_ap_att_list").html(html);
    },

    _onAddProductLine() {
        let id = this.product_line_id++;
        this.product_lines.push({
            id: id,
            product_id: '',
            description: '',
            quantity: 1,
            purpose_of_use: '',
            file_name: '',
            file_attachment: null

        });

        let productLineHtml = `
            <div id="tr_product_line_${id}" class="row mb-3 align-items-end product-line-row">
                <div class="col-md-3">
                    <label for="search_${id}" class="form-label">Product</label>
                    <div class="input-group">
                        <input type="text" class="form-control search" id="search_${id}" data_id="${id}" placeholder="Search Product">
                        <span class="input-group-text"><i class="fa fa-search"></i></span>
                        <div class="position-relative w-100">
                            <div class="c_query_sugg position-absolute w-100" style="z-index: 1050;">
                                <div id="query_sugg_id_${id}" class="query_sugg bg-white border shadow-sm w-100" style="display: none; max-height: 200px; overflow-y: auto;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <label for="description_${id}" class="form-label">Description</label>
                    <input type="text" class="form-control line_item" id="description_${id}" data_id="${id}" data_name="description" placeholder="Description">
                </div>
                <div class="col-md-2"> 
                    <label for="quantity_${id}" class="form-label">Qty</label>
                    <input type="number" class="form-control line_item line_item_quantity" id="quantity_${id}" data_id="${id}" data_name="quantity" value="1" min="1" placeholder="1">
                </div>
                <div class="col-md-2">
                    <label for="purpose_${id}" class="form-label">Purpose of Use</label>
                    <input type="text" class="form-control line_item" id="purpose_${id}" data_id="${id}" data_name="purpose_of_use" placeholder="Purpose of Use">
                </div>
                <div class="col-md-3">
                    <div class="d-flex gap-2">
                        <!-- Attach Files Button -->
                        <div class="position-relative flex-grow-1">
                            <button type="button" class="btn btn-primary attach_file_btn w-100 d-flex align-items-center justify-content-center" data_id="${id}" style="height: 38px;">
                                <i class="fa fa-paperclip me-2"></i>
                                Attach
                            </button>
                            <input type="file" id="product_line_file_${id}" class="product_line_file d-none" data_id="${id}" name="product_line_file_${id}">
                        </div>
                        
                        <!-- Remove Button -->
                        <div class="flex-grow-1">
                            <button type="button" class="btn btn-danger remove_product_line w-100 d-flex align-items-center justify-content-center" data_id="${id}" style="height: 38px;">
                                <i class="fa fa-trash me-2"></i>
                                Remove
                            </button>
                        </div>
                        
                        <!-- Files Display -->
                        <div class="flex-grow-1">
                            <button class="btn btn-outline-secondary dropdown-toggle w-100 d-flex align-items-center justify-content-center" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="height: 38px;">
                                <i class="fa fa-file me-2"></i>
                                Files
                            </button>
                            <ul class="dropdown-menu" id="product_line_files_list_${id}">
                                <li><span class="dropdown-item text-muted" id="file_status_${id}">No files attached</span></li>
                            </ul>
                        </div>

                    </div>
                </div>
            </div>
        `;

        $("#product_lines_container").append(productLineHtml);
        console.log("Added product line:", this.product_lines);
    },

    _onRemoveProductLine(ev) {
        const id = $(ev.currentTarget).attr("data_id");
        $(`#tr_product_line_${id}`).remove();
        this.product_lines = this.product_lines.filter(line => line.id != id);
        console.log("Product lines after removal:", this.product_lines);
    },

    _onLineItemChange(ev) {
        const input = $(ev.currentTarget);
        const id = input.attr("data_id");
        const field = input.attr("data_name");
        const val = input.val();
        const type = input.attr("type");

        this.product_lines.forEach(line => {
            if (line.id == id) {
                line[field] = type === "number" ? parseInt(val) : val;
            }
        });
        console.log("Updated product line:", this.product_lines);
    },

    _onSearchFocus(ev) {
        $(".query_sugg").hide();
        const id = $(ev.currentTarget).attr("data_id");
        $(`#query_sugg_id_${id}`).show();
    },

    _onSearchKeyup(ev) {
        const input = $(ev.currentTarget);
        const query = input.val();
        this.sel_line_id = input.attr("data_id");

        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            this._ajaxGetProducts(query);
        }, 300);
    },

    _ajaxGetProducts(query) {
        if (!query || query.length < 2) return;

        const id = this.sel_line_id;
        console.log("Searching for products with query:", query);

        // Show loading indicator
        $(`#query_sugg_id_${id}`).html('<div class="p-2 text-center"><i class="fa fa-spinner fa-spin"></i> Searching...</div>').show();

        $.ajax({
            url: "/ajax_requisition_get_products",
            type: "POST",
            data: {
                query: query,
                city: "Dhaka"
            },
            success: (data) => {
                console.log("Search response:", data);
                try {
                    const response = JSON.parse(data);
                    if (response.status === "success") {
                        const products = response.data;
                        if (products && products.length > 0) {
                            let suggHtml = products.map(p =>
                                `<li class="list-group-item list-group-item-action sugg_product"
                                    data_line_id="${id}" data_product_id="${p.id}">${p.name}</li>`
                            ).join('');
                            $(`#query_sugg_id_${id}`).html(`<ul class="list-group">${suggHtml}</ul>`).show();
                        } else {
                            $(`#query_sugg_id_${id}`).html('<div class="p-2 text-center">No products found</div>').show();
                        }
                    } else {
                        $(`#query_sugg_id_${id}`).html('<div class="p-2 text-center">Error: ' + response.message + '</div>').show();
                    }
                } catch (e) {
                    console.error("Error parsing response:", e);
                    $(`#query_sugg_id_${id}`).html('<div class="p-2 text-center">Error processing results</div>').show();
                }
            },
            error: (xhr, status, error) => {
                console.error("AJAX error:", error);
                $(`#query_sugg_id_${id}`).html('<div class="p-2 text-center">Error: Could not fetch products</div>').show();
            }
        });
    },

    _onSelectSuggestedProduct(ev) {
        const $el = $(ev.currentTarget);
        const productId = $el.attr("data_product_id");
        const lineId = $el.attr("data_line_id");
        const name = $el.text();

        $(`#search_${lineId}`).attr("data_product_id", productId).val(name).trigger("change");
        $('.query_sugg').hide();
    },

    _onProductChange(ev) {
        const input = $(ev.currentTarget);
        const id = input.attr("data_id");
        const productId = input.attr("data_product_id");

        this.product_lines.forEach(line => {
            if (line.id == id) {
                line.product_id = productId;
            }
        });
        console.log("Product selected:", this.product_lines);
    },

    _onAttachFileClick(ev) {
        const id = $(ev.currentTarget).attr("data_id");
        $(`#product_line_file_${id}`).click();
    },

    _onProductLineFileChange(ev) {
        const input = $(ev.currentTarget);
        const id = input.attr("data_id");
        const file = ev.target.files[0]; // Get only the first file

        if (file) {
            // Update UI to show loading
            $(`#file_status_${id}`).html(`<i class="fa fa-spinner fa-spin me-2"></i>Processing ${file.name}...`);
            
            // Update the dropdown to show the file name
            $(`#product_line_files_list_${id}`).html(`
                <li><span class="dropdown-item text-success">
                    <i class="fa fa-file me-2"></i>${file.name}
                </span></li>
            `);
            
            // Update the product line data
            this.product_lines.forEach(line => {
                if (line.id == id) {
                    line.file_name = file.name;
                    // We'll keep the actual file object for form submission
                }
            });
            
            console.log("File attached to product line:", this.product_lines);
        }
    },

    _onFormSubmit(ev) {
        console.log("Form submitted");
        let error = false;

        // Validate product selections
        const allValid = this.product_lines.every(p => {
            if (!p.product_id) {
                error = true;
                return false;
            }
            return true;
        });

        if (!allValid) {
            alert("One or more products have an invalid product_id. Please select products from the dropdown.");
            ev.preventDefault();
            return;
        }

        // Set the product_lines hidden input value - exclude the actual file objects
        const productLinesData = this.product_lines.map(line => {
            const { file_attachment, ...lineData } = line;
            return lineData;
        });
        
        $("#product_lines").val(JSON.stringify(productLinesData));
        console.log("Form submission data prepared");
    }
});

export default publicWidget.registry.ProductRequisition;