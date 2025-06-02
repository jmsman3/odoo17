# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vendor = fields.Boolean(string='Is Vendor', default=False)


class VendorLedgerReportHandler(models.AbstractModel):
    _name = 'account.vendor.ledger.report.handler'
    _inherit = 'account.partner.ledger.report.handler'
    _description = 'Vendor Ledger Report Handler'

    def _custom_options_initializer(self, report, options, previous_options=None):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        
        options['forced_domain'] = options.get('forced_domain', []) + [('partner_id.is_vendor', '=', True)]