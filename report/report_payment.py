# -*- coding: utf-8 -*-

from odoo import api, models
import odoo.addons.l10n_sv.a_letras

class ReportAbstractPayment(models.AbstractModel):
    _name = 'onlife.abstract.reporte_account_payment'

    nombre_reporte = ''

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'account.payment'
        docs = self.env[self.model].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'a_letras': odoo.addons.l10n_sv.a_letras,
        }

class ReportPayment1(models.AbstractModel):
    _name = 'report.onlife.reporte_account_payment1'
    _inherit = 'onlife.abstract.reporte_account_payment'

    nombre_reporte = 'onlife.reporte_account_payment1'
