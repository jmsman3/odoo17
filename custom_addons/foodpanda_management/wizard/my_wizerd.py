from odoo import models, fields, api
from odoo.exceptions import UserError

class SetChefAvailability(models.TransientModel):
    _name = 'set.chef.availability.wizard'
    _description = 'Set Chef Availability Wizard'

    chef_id = fields.Many2one('foodpanda.chef', string="Chef", required=True)
    is_available = fields.Boolean(string="Available?", default=True)
    note = fields.Text(string="Optional Note")

    def action_set_availability(self):
        if not self.chef_id:
            raise UserError("Chef must be selected.")
        self.chef_id.write({
            'is_available': self.is_available,
            'note': self.note
        })
        return {'type': 'ir.actions.act_window_close'}
