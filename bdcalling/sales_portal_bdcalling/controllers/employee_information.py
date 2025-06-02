from odoo import http
from odoo.http import request as req

class PortalEmployeeInfo(http.Controller):

    @http.route('/portal/employees', type='http', auth='user', website=True)
    def portal_employees(self, **kw):
        user = req.env.user
        user_id = user.id

        if not user_id:
            return 'User ID not found'

        # Get the employee linked to the current user
        employee = req.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)

        if not employee:
            return 'Employee not found'

        # Handle search and pagination
        search_value = kw.get('search_value', '')
        page = int(kw.get('page', 1))
        per_page = 10
        offset = (page - 1) * per_page

        # Filter by same company
        domain = [('company_id', '=', employee.company_id.id)]
        if search_value:
            domain += ['|', ('name', 'ilike', search_value), ('work_email', 'ilike', search_value)]

        employees = req.env['hr.employee'].sudo().search(domain, limit=per_page, offset=offset)
        total_count = req.env['hr.employee'].sudo().search_count(domain)
        total_pages = (total_count + per_page - 1) // per_page

        values = {
            'employee': employee,
            'employees': employees,
            'search_value': search_value,
            'page': page,
            'total_pages': total_pages,
        }

        return req.render('sales_portal_bdcalling.portal_employees_template', values)
