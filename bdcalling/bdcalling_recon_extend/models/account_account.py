from odoo import fields, models, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    bank_type = fields.Selection([
        ('fiverr', 'Fiverr'),
        ('upwork', 'UpWork'),
        ('payoneer', 'Payoneer'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank'),
        ('e-wallet', 'E-Wallet'),
        ('paypal', 'PayPal'),
        ('other', 'Other')
    ], string='Bank Type')


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_type = fields.Selection([
        ('fiverr', 'Fiverr'),
        ('upwork', 'UpWork'),
        ('payoneer', 'Payoneer'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank'),
        ('e-wallet', 'E-Wallet'),
        ('paypal', 'PayPal'),
        ('other', 'Other')
    ], string='Bank Type')

    @api.model
    def _prepare_liquidity_account_vals(self, company, code, vals):
        return {
            'name': vals.get('name'),
            'code': code,
            'bank_type': vals.get('bank_type'),
            'account_type': 'asset_cash',
            'currency_id': vals.get('currency_id'),
            'company_id': company.id,
        }