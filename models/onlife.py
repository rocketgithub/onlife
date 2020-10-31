# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

class Laboratorio(models.Model):
    _name = "onlife.laboratorio"

    name = fields.Char('Nombre', required=True)

    _sql_constraints = [
        ('code_value_uniq', 'unique (name)', 'El nombre del laboratorio debe ser único !')
    ]

class CampoPersonalizado(models.Model):
    _name = "onlife.campo_personalizado"
    
    name = fields.Char('Nombre', required=True)

class ProductoCampoPersonalizado(models.Model):
    _name = "onlife.producto_campo_personalizado"
    _rec_name = 'product_id'

    def _campos_personalizados(self):
        res = []
        fields = self.env['onlife.campo_personalizado'].search([])
        for field in fields:
            res.append((field.name, field.name))
        return res

    product_id = fields.Many2one('product.template', string='Producto', required=True, ondelete='cascade', index=True, copy=False)
    campo_personalizado_id = fields.Selection(selection=_campos_personalizados, string='Campo personalizado', required=True, store=True)
    value = fields.Char('Valor', required=True)

    _sql_constraints = [
        ('code_value_uniq', 'unique (campo_personalizado_id, product_id)', 'El campo personalizado debe ser único por producto !')
    ]

