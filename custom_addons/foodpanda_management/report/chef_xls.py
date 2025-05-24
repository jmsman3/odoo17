from odoo import models

from xlsxwriter.workbook import Workbook




from odoo import models

class ChefCardXlsx(models.AbstractModel):
    _name = 'report.foodpanda_management.report_chef_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, chefs):
        format_header = workbook.add_format({
            'font_size': 12, 'bold': True, 'align': 'center',
            'bg_color': '#D3D3D3', 'border': 1})
        
        format_cell = workbook.add_format({
            'font_size': 10, 'align': 'center', 'border': 1
        })

        sheet = workbook.add_worksheet('Chef Card')
        sheet.set_column('A:I', 20)

        # aita only Header
        headers = [
            'Name', 'Speciality', 'Experience', 'Rating',
            'Phone', 'Email', 'Available?', 'Active?', 'Notes'
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, format_header)

        row = 1
        for chef in chefs:
            sheet.write(row, 0, chef.name or '', format_cell)
            sheet.write(row, 1, chef.speciality or '', format_cell)
            sheet.write(row, 2, chef.experience_years or 0, format_cell)
            sheet.write(row, 3, chef.rating or 0.0, format_cell)
            sheet.write(row, 4, chef.phone or '', format_cell)
            sheet.write(row, 5, chef.email or '', format_cell)
            sheet.write(row, 6, 'Yes' if chef.is_available else 'No', format_cell)
            sheet.write(row, 7, 'Yes' if chef.active else 'No', format_cell)
            sheet.write(row, 8, chef.note or '', format_cell)
            row += 1 

        # prottekta Data Row
        # sheet.write(1, 0, chef.name or '', format_cell)
        # sheet.write(1, 1, chef.speciality or '', format_cell)
        # sheet.write(1, 2, chef.experience_years or 0, format_cell)
        # sheet.write(1, 3, chef.rating or 0.0, format_cell)
        # sheet.write(1, 4, chef.phone or '', format_cell)
        # sheet.write(1, 5, chef.email or '', format_cell)
        # sheet.write(1, 6, 'Yes' if chef.is_available else 'No', format_cell)
        # sheet.write(1, 7, 'Yes' if chef.active else 'No', format_cell)
        # sheet.write(1, 8, chef.note or '', format_cell) 

 




# class ChefCardXlsx(models.AbstractModel):
#     _name = 'report.foodpanda_management.report_chef_xls'
#     _inherit= 'report.report_xlsx.abstract'

#     def make_xlsx_report(self, workbook, data , lines):
#         format1 = workbook.add_format({'font_size': 15 , 'align': 'vcenter' , 'bold': True })
#         format2 = workbook.add_format({'font_size': 10 , 'align': 'vcenter' , 'border': 2})


#         sheet = workbook.add_worksheet('Chef Card')

#         sheet.set_column('B:C', 20)

    
    
#         sheet.write(2,1, 'name', format1)
#         sheet.write(2,2, lines.name or '', format2)


#         sheet.write(3,1, 'speciality', format1)
#         sheet.write(3,2, lines.speciality or '', format2)


#         sheet.write(4,1, 'experience_years', format1)
#         sheet.write(4,2, lines.experience_years or '', format2)



#         sheet.write(5,1, 'rating', format1)
#         sheet.write(5,2, lines.rating or '', format2)



#         sheet.write(6,1, 'phone', format1)
#         sheet.write(6,2, lines.phone or '', format2)


#         sheet.write(7,1, 'email', format1)
#         sheet.write(7,2, lines.email or '', format2)
    
    


