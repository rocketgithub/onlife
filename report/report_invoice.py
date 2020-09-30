# -*- coding: utf-8 -*-

from odoo import api, models
import re
import odoo.addons.l10n_sv.a_letras
import logging

class ReportAbstractInvoice(models.AbstractModel):
    _name = 'onlife.abstract.reporte_account_invoice'

    nombre_reporte = ''

    def total_linea(self, l):
        currency = l.move_id and l.move_id.currency_id or None
        price_unit = l.price_unit * (1 - (l.discount or 0.0) / 100.0)
        taxes = l.tax_ids.compute_all(price_unit, currency, l.quantity, l.product_id, l.move_id.partner_id)
        price_total = taxes['total_included']
        timbre = 0
        for tax in taxes['taxes']:
            if tax['name'] == 'Timbre de Prensa Ventas':
                price_total -= tax['amount']
        return price_total

    def total_linea_con_impuesto(self, l):
        currency = l.move_id and l.move_id.currency_id or None
        price_unit = l.price_unit * (1 - (l.discount or 0.0) / 100.0)
        taxes = l.tax_ids.compute_all(price_unit, currency, l.quantity, l.product_id, l.move_id.partner_id)
        price_total = l.price_total
        for tax in taxes['taxes']:
            if tax['name'] == 'Timbre de Prensa Ventas':
                price_total -= tax['amount']
        return price_total

    def impuesto_impresos(self, o):
        impuestos = []
        for tax in o.amount_by_group:
            if tax[0] == 'Timbre de Prensa Ventas':
                impuestos.append({'nombre': 'Timbre de Prensa', 'valor': tax[1]})
        return impuestos


    def valor_retencion_iva(self, o):
        valor = 0
        for tax in o.amount_by_group:
            if tax[0] == 'Retención IVA':
                valor = tax[1]
        return valor

    def total_descuento(self, o):
        t = 0
        for l in o.invoice_line_ids:
            t += ( l.price_unit * l.discount/100 ) * l.quantity
        return t

    def producto(self, nombre):
        return re.sub(r'\[\w+\] ', '', nombre)

    def producto_completo(self, line, tamano):
        nombre = re.sub(r'\[\w+\] ', '', line.name)
        if tamano > 0:
            nombre = nombre[0:tamano]
        if line.discount > 0:
            nombre += ' Descuento (' + str(line.discount) + ')'

        nombre += ' Lote: ' + line.lote
#        stock_move = self.env['stock.move'].search([('picking_id.origin', '=', line.invoice_id.origin), ('product_id', '=', line.product_id.id)])
#        if stock_move:
#            lote = ''
#            x = 0
#            for move_line in stock_move.move_line_ids:
#                if move_line.lot_id:
#                    if x > 0:
#                        lote += ', '
#                    lote += move_line.lot_id.name
#                    if move_line.lot_id.life_date:
#                        lote += ' V: ' + str(move_line.lot_id.life_date)
#                    x += 1
#            if lote != '':
#                nombre += ' Lote: ' + lote

        return nombre

    def producto_completo2(self, line):
        nombre = re.sub(r'\[\w+\] ', '', line['name'])
        nombre += ' ' + line['lote']
        if line['discount'] > 0:
            nombre += ' - Descuento ' + str(line['discount']) + '%'

        return nombre

    def venta_total(self, o):
        return o.amount_total + self.valor_retencion_iva(o)

    def descuento_report6(self, o):
        descuento = 0
        for linea in o.invoice_line_ids:
            if linea.discount > 0:
                if linea.discount == 100:
                    r = linea.invoice_line_tax_ids.compute_all(linea['price_unit'], currency=o.currency_id, quantity=linea.quantity, product=linea.product_id, partner=o.partner_id)
                    descuento += r['base'] - linea.price_subtotal
                else:
                    descuento += ( linea.price_subtotal / (1 - (linea.discount/100)) ) - linea.price_subtotal
        return descuento

    def lineas_report6(self, o):
        res = []
        for linea in o.invoice_line_ids:
            dict = {}
            dict['name'] = linea.product_id.name
            dict['lote'] = linea.lote
            dict['quantity'] = linea.quantity
            dict['discount'] = linea.discount
            if linea.discount == 100:
                r = linea.invoice_line_tax_ids.compute_all(linea['price_unit'], currency=o.currency_id, quantity=linea.quantity, product=linea.product_id, partner=o.partner_id)
                dict['price_subtotal'] = r['base'];
            else:
                dict['price_subtotal'] = linea.price_subtotal / (1 - (linea.discount/100))
            dict['price_unit'] = (dict['price_subtotal'] / dict['quantity'])
            res.append(dict)
        return res

    def lineas_report7(self, o):
        res = []
        product_id = ''
        for linea in o.invoice_line_ids:
            dict = {}
            if linea.discount == 100:
                r = linea.invoice_line_tax_ids.compute_all(linea['price_unit'], currency=o.currency_id, quantity=linea.quantity, product=linea.product_id, partner=o.partner_id)
                descuento = r['base'] - linea.price_subtotal
            else:
                descuento = ( linea.price_subtotal / (1 - (linea.discount/100)) ) - linea.price_subtotal

            if linea.product_id.id == product_id:
                factor_multiplicador = -1
                res[len(res)-1]['quantity'] += linea.quantity
                res[len(res)-1]['price_subtotal'] += descuento
                res[len(res)-1]['price_unit'] += res[len(res)-1]['price_subtotal'] / res[len(res)-1]['quantity']
                dict['price_subtotal'] = descuento * factor_multiplicador
            else:
                factor_multiplicador = 1
                dict['price_subtotal'] = linea.price_subtotal * factor_multiplicador

            dict['name'] = linea.product_id.name
            dict['lote'] = linea.lote
            dict['quantity'] = linea.quantity
            dict['discount'] = linea.discount
            dict['price_unit'] = (dict['price_subtotal']/linea.quantity)
            res.append(dict)
            product_id = linea.product_id.id
        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'account.move'
        docs = self.env[self.model].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'a_letras': odoo.addons.l10n_sv.a_letras,
            'total_descuento': self.total_descuento,
            'producto': self.producto,
            'producto_completo': self.producto_completo,
            'producto_completo2': self.producto_completo2,
            'total_linea': self.total_linea,
            'impuesto_impresos': self.impuesto_impresos,
            'valor_retencion_iva': self.valor_retencion_iva,
            'venta_total': self.venta_total,
            'total_linea_con_impuesto': self.total_linea_con_impuesto,
            'descuento_report6': self.descuento_report6,
            'lineas_report6': self.lineas_report6,
            'lineas_report7': self.lineas_report7,
        }


class ReportInvoice1(models.AbstractModel):
    _name = 'report.onlife.reporte_account_invoice1'
    _inherit = 'onlife.abstract.reporte_account_invoice'

    nombre_reporte = 'onlife.reporte_account_invoice1'

class ReportInvoice2(models.AbstractModel):
    _name = 'report.onlife.reporte_account_invoice2'
    _inherit = 'onlife.abstract.reporte_account_invoice'

    nombre_reporte = 'onlife.reporte_account_invoice2'
