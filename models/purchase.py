# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    descuento = fields.Float(string='Descuento (%)', digits='Discount', default=0.0)
    
    def _prepare_compute_all_values(self):
        vals = super(PurchaseOrderLine, self)._prepare_compute_all_values()
        vals['price_unit'] = vals['price_unit'] * (1 - (self.descuento / 100))
        return vals
