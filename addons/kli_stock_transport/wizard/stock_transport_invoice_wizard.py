# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2020  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Anggar Bagus Kurniawan <anggar.bagus@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.addons import decimal_precision as dp
import time
import os, base64, xlrd
import logging
_logger = logging.getLogger(__name__)

class StockTransportInvoiceWizard(models.TransientModel):
    _name = "stock.transport.invoice.wizard"
    _description = "Transport Invoice Creation Wizard"

    partner_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier','=',True)], required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    date_start = fields.Date('Date Start', required=True)
    date_end = fields.Date('Date End', required=True)
    journal_id = fields.Many2one('account.journal', required=True, string='Journal', domain=[('type','=','purchase')])


    @api.multi
    def create_invoice(self):
        for record in self:
            warning = ''
            invoice_lines = []
            per_product = {}
            transport = self.env['stock.transport.move'].search([
                ('partner_id', '=', record.partner_id.id),
                ('product_id', '=', record.product_id.id),
                ('date', '>=', record.date_start),
                ('date', '<=', record.date_end),
                ('invoiced', '=', False)
                ])
            if not transport:
                raise Warning('Data tidak ditemukan!')
            
            for trans in transport:
                # Grouping per product
                if not per_product.get(trans.product_id.id, False):
                    per_product[trans.product_id.id] = {}
                    per_product[trans.product_id.id]['amount'] = 0
                per_product[trans.product_id.id]['amount'] = per_product[trans.product_id.id].get('amount',0)+trans.price_unit*trans.product_qty
                trans.write({'invoiced': True})

            # Set invoice lines
            for key, item in per_product.items():
                # Invoice Lines
                invoice_lines.append(
                    [0,0,{
                    'name': self.env['product.product'].browse(key).name,
                    'product_id': key,
                    'quantity': 1,
                    'price_unit': item['amount'],
                    'account_id': record.partner_id.property_account_payable_id.id,
                    }])


            # Create Invoice
            if invoice_lines:
                invoice = {
                'partner_id': record.partner_id.id,
                'date_invoice': fields.Date.context_today(self),
                'journal_id': record.journal_id.id,
                'account_id': record.journal_id.default_credit_account_id.id,
                'type': 'in_invoice',
                'invoice_line_ids': invoice_lines,
                }
                invoice_id=self.env['account.invoice'].sudo().create(invoice)

                return {
                    'domain': [('id', 'in', [invoice_id.id])],
                    'name': 'Created Invoice Transport',
                    'view_mode': 'tree,form',
                    'res_model': 'account.invoice',
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                }
