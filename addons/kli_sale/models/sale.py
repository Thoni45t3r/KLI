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

    price_statement_rule    = fields.Char("Peraturan Pemerintah")
    source_warehouse_note   = fields.Text("Asal Barang")
    picking_location_note   = fields.Text("Lokasi Pemuatan")
    delivery_of_goods       = fields.Text("Penyerahan")
    quantity_note           = fields.Text("Catatan Kuantitas")
    quality_ffa             = fields.Char("FFA")
    quality_mni             = fields.Char("M & I")
    quality_iv              = fields.Char("IV (WIJS)")
    quality_claim           = fields.Text("Perhitungan Klaim")
    quality_note            = fields.Text("Catatan Kualitas")
    other_claim             = fields.Text("Lain - lain")
    payment_term_note       = fields.Text("Pembayaran")
    partner_bank_id         = fields.Many2one("res.partner.bank", string="Bank Payment")
    ppn_include             = fields.Boolean(string="Include PPN")
    sign_seller             = fields.Char("Ttd Penjual", default="ROSDIANA")
    sign_buyer              = fields.Char("Ttd Pembeli", default="PEMBELI")
    sign_seller_position    = fields.Char("Jabatan Penjual")
    sign_buyer_position     = fields.Char("Jabatan Pembeli")

    @api.onchange('doc_type_id')
    def onchange_document_type_sale_sjm(self):
        if self.doc_type_id:
            self.price_statement_rule   = self.doc_type_id.price_statement_rule or False
            self.delivery_of_goods      = self.doc_type_id.delivery_of_goods or False
            self.quantity_note          = self.doc_type_id.quantity_note or False
            self.quality_ffa            = self.doc_type_id.quality_ffa or False
            self.quality_mni            = self.doc_type_id.quality_mni or False
            self.quality_iv             = self.doc_type_id.quality_iv or False
            self.quality_claim          = self.doc_type_id.quality_claim or False
            self.quality_note           = self.doc_type_id.quality_note or False
            self.other_claim            = self.doc_type_id.other_claim or False
            self.payment_term_note      = self.doc_type_id.payment_term_note or False
            self.partner_bank_id        = self.doc_type_id.partner_bank_id and self.doc_type_id.partner_bank_id.id or False
            self.ppn_include            = self.doc_type_id.ppn_include or False
            self.sign_seller            = self.doc_type_id.sign_seller or False
            self.sign_buyer             = self.doc_type_id.sign_buyer or False