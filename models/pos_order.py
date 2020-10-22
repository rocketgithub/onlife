# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
import logging

class PosOrder(models.Model):
    _inherit = "pos.order"

    invoice_journal_id = fields.Many2one('account.journal', string='Diario factura')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        if 'invoice_journal_id' in ui_order.keys():
            res['invoice_journal_id'] = ui_order['invoice_journal_id']
        return res

    def _prepare_invoice_vals(self):
        vals = super(PosOrder, self)._prepare_invoice_vals()
        if self.invoice_journal_id:
            vals['journal_id'] = self.invoice_journal_id.id
        return vals
