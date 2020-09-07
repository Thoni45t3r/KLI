# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2018  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Hendra Saputra <hendrasaputra0501@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    @api.multi
    def create_report_kli(self):
        user = self.env.user
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'report_purchase_request_kli',
            'datas': {
                'model': 'purchase.request',
                'id': self._context.get('active_ids') and self._context.get('active_ids')[0] or self.id,
                'ids': self._context.get('active_ids') and self._context.get('active_ids') or [],
                'report_type': 'xlsx',
                'name': self.name or "---",
                'user': user.partner_id.name or user.login
            },
            'nodestroy': False
        }
class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    status_barang = fields.Char('Status Barang')
    keterangan = fields.Char('Lokasi Pemakaian & Keterangan')
    budget_remarks = fields.Char('Ket. Budget')
    budget_price_unit = fields.Float('Budget Harga Satuan')
    keterangan_po = fields.Char('Ket. PO')