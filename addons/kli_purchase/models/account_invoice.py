from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        default_location_type = self.env['account.location.type'].search([('code','=','NA')])
        if default_location_type:
            data['account_location_type_id'] = default_location_type.id
        return data