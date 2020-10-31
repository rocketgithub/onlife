# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

class ProductTemplate(models.Model):
    _inherit = "product.template"

    laboratorio_id = fields.Many2one('onlife.laboratorio', 'Laboratorio')
    keywords = fields.Char('Search keywords')
    campo_personalizado_ids = fields.One2many('onlife.producto_campo_personalizado', 'product_id', 'Campo personalizado')
