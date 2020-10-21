# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging

class PosConfig(models.Model):
    _inherit = 'pos.config'

    invoice_journal_ids = fields.Many2many('account.journal', string='Diarios de factura')

    def obtener_diarios(self, condiciones, campos):
        config = self.env['account.journal'].sudo().search_read(condiciones, [])
        return config

