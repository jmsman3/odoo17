# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    order = fields.Char(string='Order')
    gig = fields.Char(string='Gig')
    service_type = fields.Char(string='Order or Service Type')
    seller = fields.Char(string='Seller')
    provider = fields.Char(string='Provider')
    transaction = fields.Char(string='Transaction ID')
    team = fields.Char(string='Team')


class BankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    order = fields.Char(string='Order')
    gig = fields.Char(string='Gig')
    service_type = fields.Char(string='Order or Service Type')
    seller = fields.Char(string='Seller')
    provider = fields.Char(string='Provider')
    transaction = fields.Char(string='Transaction ID')
    team = fields.Char(string='Team')
    entry_by = fields.Char(string='Entry By')
    @api.model
    def create(self, vals):
        new_line = super(BankStatementLine, self).create(vals)
        if new_line.move_id:
            new_line.move_id.update({
                'order': new_line.order,
                'gig': new_line.gig,
                'transaction': new_line.transaction,
                'service_type': new_line.service_type,
                'seller': new_line.seller,
                'provider': new_line.provider,
                'team': new_line.team,

            })
        return new_line

    def write(self, vals):
        result = super(BankStatementLine, self).write(vals)
        for line in self:
            if line.move_id:
                line.move_id.update({
                    'order': line.order,
                    'gig': line.gig,
                    'transaction': line.transaction,
                    'service_type': line.service_type,
                    'seller': line.seller,
                    'provider': line.provider,
                    'team': line.team,
                })
        return result




