# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2018  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Hendra Saputra <hendrasaputra0501@gmail.com>
#   @modified Deby Wahyu Kurdian <deby.wahyu.kurdian@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    skb = fields.Boolean("Is SKB?")

    @api.model
    def default_get(self, fields):
        res = super(StockPicking, self).default_get(fields)
        picking_type_ids = self.env['stock.picking.type'].search([('code','=','internal'),
                ('return_picking_type_id','!=',False),
                ('default_location_src_id.usage','=','internal'),
                ('default_location_dest_id.usage','!=','internal')])
        if res.get('skb', False):
            res['picking_type_id'] = picking_type_ids[-1].id if picking_type_ids else False
        return res

    @api.multi
    def print_report_picking(self):
        return {
                'type'          : 'ir.actions.report.xml',
                'report_name'   : 'report_stock_picking',
                'datas'         : {
                    'model'         : 'stock.picking',
                    'id'            : self._context.get('active_ids') and self._context.get('active_ids')[0] or self.id,
                    'ids'           : self._context.get('active_ids') and self._context.get('active_ids') or [],
                    'name'          : self.name or "---",
                    },
                'nodestroy'     : False
        }