import logging
from odoo import http
from odoo.http import request
import base64
_logger = logging.getLogger(__name__)

class CustomerController(http.Controller):

    @http.route('/customer/form', type='http', auth="user", website=True)
    def customer_form(self, **kwargs):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        if not employee:
            return request.redirect('/my/home')

        return request.render('sales_portal_bdcalling.customer_form_template')
    

    @http.route('/customer/submit', type='json', auth="user", website=True, csrf=False)
    def customer_submit(self, **post):
        try:
            _logger.info(f"Received data: {post}")

            user = request.env.user
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

            # Ensure the user company is set
            company_id = request.env.company
            print('company_id:', company_id)
            print("Company Name:", company_id.name)
            if not employee:
                return {'success': False, 'error': 'Invalid user'}

            # Extract Data
            name = post.get('partner_name')
            # email = post.get('partner_email')
            # phone = post.get('partner_phone')
            # address = post.get('partner_address')
            # city = post.get('partner_city')
            zip_code = post.get('partner_zip')
            country_name = post.get('partner_country')
            partner_id = post.get('partner_id')
            # image_1920 = post.get('image_1920')
            # Log the extracted data
            _logger.info(f"Extracted data: name={name}, "  # email={email}, phone={phone},
                        #  f"address={address}, city={city}, zip_code={zip_code}, "
                         f"country_name={country_name}, partner_id={partner_id}")

            # Validate Required Fields
            if not name:
                return {'success': False, 'error': "Customer name is required"}
            
            if not country_name:
                return {'success': False, 'error': "Country name is required"}

            # Find Country
            country = request.env['res.country'].sudo().search([('name', 'ilike', country_name)], limit=1)
            if not country:
                return {'success': False, 'error': f"Country '{country_name}' not found"}
            
            # Validate phone only if provided
            # if phone:
            #     existing_partner_phone = request.env['res.partner'].sudo().search([('phone', '=', phone)], limit=1)
            #     if existing_partner_phone:
            #         return {
            #             'success': False,
            #             'error': f"Phone number already exists for customer {existing_partner_phone.name}"
            #         }

            # # Validate email only if provided
            # if email:
            #     existing_partner_email = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            #     if existing_partner_email:
            #         return {
            #             'success': False,
            #             'error': f"Email already exists for customer {existing_partner_email.name}"
            #         }

            # image_data = None
            # if image_1920:
            #     try:
            #         image_data = base64.b64decode(image_1920)
            #     except Exception as img_error:
            #         _logger.error(f"Error decoding image: {str(img_error)}")
            #         return {'success': False, 'error': 'Invalid image data'}

            customer_vals = {
                'name': name,
                # 'email': email,
                # 'phone': phone,
                # 'street': address,
                # 'city': city,
                'zip': zip_code,
                'country_id': country.id,
                # 'company_id': company_id.id, #customer added by user company 
            }
            # if image_data:
            #     customer_vals['image_1920'] = image_1920  # Store base64 image

            customer = request.env['res.partner'].sudo().create(customer_vals)
            _logger.info(f"Customer created successfully: {customer.id} - {customer_vals}")
            return {'success': True, 'message': f"Customer {customer.name}  created successfully at {company_id.name}", 'redirect_url': '/shop/dashboard'}

        except Exception as e:
            _logger.error(f"Error while creating customer: {str(e)}", exc_info=True)
            return {'success': False, 'error': "An error occurred while processing the request."}