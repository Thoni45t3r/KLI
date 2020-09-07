from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit    = ['purchase.order']

    @api.multi
    def print_report_purchase(self):
        return {
            'type'          : 'ir.actions.report.xml',
            'report_name'   : 'report_purchase_order_sparepart',
            'datas'         : {
                'model'         : 'purchase.order',
                'id'            : self.id,
                'ids'           : self._context.get('active_ids') and self._context.get('active_ids') or [],
                'name'          : self.name or "---",
                },
            'nodestroy'     : False
        }