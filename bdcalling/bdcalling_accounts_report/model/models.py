# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def amount_to_text(self, amount):
        from num2words import num2words
        amount_in_words = num2words(amount, lang='en').capitalize()
        return f"{amount_in_words} Taka Only."

