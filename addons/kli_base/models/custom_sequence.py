# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2018  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Deby Wahyu Kurdian <deby.wahyu.kurdian@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit    = ['sale.order']

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res.partner_id and res.name:
            if res.name.find('custom_partner') > 0:
                partner_code    = str(res.partner_id.partner_code) if str(res.partner_id.partner_code) != 'False' else "SO"
                new_name        = res.name.replace(res.name[(res.name.find('custom_partner')):(res.name.find('custom_partner'))+14], str(partner_code))
                if res.name:
                    res.name = new_name
        return res

class PurchaseOrder(models.Model):
    _inherit    = ['purchase.order']

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        if res.partner_id and res.name:
            if res.name.find('custom_partner') > 0:
                partner_code    = str(res.partner_id.partner_code) if str(res.partner_id.partner_code) != 'False' else "PO"
                new_name        = res.name.replace(res.name[(res.name.find('custom_partner')):(res.name.find('custom_partner'))+14], str(partner_code))
                if res.name:
                    res.name = new_name
        return res

class AccountInvoice(models.Model):
    _inherit    = ['account.invoice']

    @api.multi
    def _write(self, vals):
        for invoice in self:
            new_number  = False
            if invoice.partner_id and vals.get('number', False):
                if vals.get('number', False).find('custom_partner') > 0:
                    partner_code    = str(invoice.partner_id.partner_code) if str(invoice.partner_id.partner_code) != 'False' else "INV"
                    new_number      = vals.get('number', False).replace(vals.get('number', False)[(vals.get('number', False).find('custom_partner')):(vals.get('number', False).find('custom_partner'))+14], str(partner_code))
                    if vals.get('number', False):
                        vals.update({'number' : new_number, 'move_name' : new_number})
            if invoice.move_id.name != new_number and new_number:
                invoice.move_id.write({'name' : new_number})
        res = super(AccountInvoice, self)._write(vals)
        return res

class AccountInvoiceAdvance(models.Model):
    _inherit    = ['account.invoice.advance']

    @api.multi
    def action_invoice_open(self):
        new_number  = False
        res = super(AccountInvoiceAdvance, self).action_invoice_open()
        if self.partner_id and self.number:
            if self.number.find('custom_partner') > 0:
                partner_code    = str(self.partner_id.partner_code) if str(self.partner_id.partner_code) != 'False' else "INV-ADV"
                new_number      = self.number.replace(self.number[(self.number.find('custom_partner')):(self.number.find('custom_partner'))+14], str(partner_code))
        if new_number:
            self.number         = new_number
            self.move_id.name   = new_number
            self.move_name      = new_number
        return res