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
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.addons import decimal_precision as dp
import time

class StockTransportMove(models.Model):
    _name = "stock.transport.move"
    _description = "Transport Move"

    partner_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier','=',True)], required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    date = fields.Date('Date', required=True)
    src_location_id = fields.Many2one('stock.transport.location', string='Asal Lokasi', required=True)
    dest_location_id = fields.Many2one('stock.transport.location', string='Tujuan Lokasi', required=True)
    rate_type = fields.Selection([('by_weight','By Weight'),('by_delivery','By Delivery'),('by_distance','By Distance')], string='Rate Type', required=True)
    product_qty = fields.Float(required=True)
    accrued = fields.Boolean()
    invoiced = fields.Boolean()
    move_id = fields.Many2one('account.move', string='Journal Entry')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    price_unit = fields.Float()
    

   