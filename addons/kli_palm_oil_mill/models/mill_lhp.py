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

class MillLhp(models.Model):
    _name = "mill.lhp"
    _description = "Laporan Harian Produksi"
    _rec_name = "date"

    @api.depends('saldo_awal_tbs_brutto','saldo_awal_tbs_netto','tbs_in_brutto','tbs_in_brutto', 'tanpa_produksi')
    def _compute_tbs(self):
        for lhp in self:
            total_tbs_netto = lhp.saldo_awal_tbs_netto+lhp.tbs_in_netto
            total_tbs_brutto = lhp.saldo_awal_tbs_brutto+lhp.tbs_in_brutto

            # Lori dihitung hanya ketika ada produksi
            per_lori_netto = lhp.total_lori and total_tbs_netto/lhp.total_lori or 0.0
            per_lori_brutto = lhp.total_lori and total_tbs_brutto/lhp.total_lori or 0.0
            tbs_ramp_brutto = per_lori_brutto*lhp.restan_loading_ramp
            tbs_ramp_netto = per_lori_netto*lhp.restan_loading_ramp
            tbs_lori_brutto = per_lori_brutto*lhp.restan_lori
            tbs_lori_netto = per_lori_netto*lhp.restan_lori
            tbs_rebusan_brutto = per_lori_brutto*lhp.restan_rebusan
            tbs_rebusan_netto = per_lori_netto*lhp.restan_rebusan

            if lhp.tanpa_produksi:
                saldo_akhir_tbs_netto = total_tbs_netto
                saldo_akhir_tbs_brutto = total_tbs_brutto
            else:
                saldo_akhir_tbs_netto = tbs_ramp_netto+tbs_lori_netto+tbs_rebusan_netto
                saldo_akhir_tbs_brutto = tbs_ramp_brutto+tbs_lori_brutto+tbs_rebusan_brutto
            
            tbs_proses_brutto = per_lori_brutto*lhp.proses_tbs
            tbs_proses_netto = per_lori_netto*lhp.proses_tbs
            lhp.update({
                'total_tbs_netto': total_tbs_netto,
                'total_tbs_brutto': total_tbs_brutto,
                'per_lori_netto': per_lori_netto,
                'per_lori_brutto': per_lori_brutto,
                'tbs_ramp_brutto': tbs_ramp_brutto,
                'tbs_ramp_netto': tbs_ramp_netto,
                'tbs_lori_brutto': tbs_lori_brutto,
                'tbs_lori_netto': tbs_lori_netto,
                'tbs_rebusan_brutto': tbs_rebusan_brutto,
                'tbs_rebusan_netto': tbs_rebusan_netto,
                'saldo_akhir_tbs_netto': saldo_akhir_tbs_netto,
                'saldo_akhir_tbs_brutto': saldo_akhir_tbs_brutto,
                'tbs_proses_brutto': tbs_proses_brutto,
                'tbs_proses_netto': tbs_proses_netto

                })

    state = fields.Selection([('draft','Draft'),('approved','Approved')], default='draft')
    date = fields.Date('Tanggal')
    tanpa_produksi = fields.Boolean('Tanpa Produksi')
    lhp_tbs_line = fields.One2many('mill.lhp.tbs.line','lhp_id', string='TBS')
    lhp_cpo_line = fields.One2many('mill.lhp.cpo.line','lhp_id', string='CPO')
    proses_tbs = fields.Float('PROSES TBS')
    proses_tbs_brutto_rel = fields.Float(related='proses_tbs')
    proses_tbs_netto_rel = fields.Float(related='proses_tbs')
    restan_rebusan = fields.Float()
    restan_lori = fields.Float()
    restan_loading_ramp = fields.Float()
    restan_lantai = fields.Float()
    total_restan = fields.Float()
    total_lori = fields.Float()
    total_lori_brutto_rel = fields.Float(related='total_lori')
    total_lori_netto_rel = fields.Float(related='total_lori')
    per_lori_netto = fields.Float(compute='_compute_tbs', store=True)
    per_lori_brutto = fields.Float(compute='_compute_tbs', store=True)
    per_lori_netto_rel = fields.Float(related='per_lori_netto')
    per_lori_brutto_rel = fields.Float(related='per_lori_brutto')
    saldo_awal_tbs_brutto = fields.Float()
    saldo_awal_tbs_netto = fields.Float()
    tbs_proses_brutto = fields.Float(compute='_compute_tbs', store=True)
    tbs_proses_netto = fields.Float(compute='_compute_tbs', store=True)
    tbs_in_brutto = fields.Float()
    tbs_in_netto = fields.Float()
    total_tbs_netto = fields.Float(compute='_compute_tbs', store=True)
    total_tbs_brutto = fields.Float(compute='_compute_tbs', store=True)
    tbs_ramp_brutto = fields.Float(compute='_compute_tbs', store=True)
    tbs_ramp_netto = fields.Float(compute='_compute_tbs', store=True)
    tbs_lori_netto = fields.Float(compute='_compute_tbs', store=True)
    tbs_lori_brutto = fields.Float(compute='_compute_tbs', store=True)
    tbs_rebusan_brutto = fields.Float(compute='_compute_tbs', store=True)
    tbs_rebusan_netto = fields.Float(compute='_compute_tbs', store=True)
    saldo_akhir_tbs_netto = fields.Float(compute='_compute_tbs', store=True)
    saldo_akhir_tbs_brutto = fields.Float(compute='_compute_tbs', store=True)
    sounding_id = fields.Many2one('mill.daily.sounding')

    lhp_kernel_line = fields.One2many('mill.lhp.kernel.line','lhp_id', string='Kernel')

    # total_cpo_tangki = fields.Integer('Stock CPO Dalam Tangki')
    total_cpo_tangki = fields.Float('Stock CPO Dalam Tangki')
    # total_pengiriman_cpo = fields.Integer('Pengiriman CPO')
    total_pengiriman_cpo = fields.Float('Pengiriman CPO')
    # saldo_awal_cpo = fields.Integer('Saldo Awal CPO')
    saldo_awal_cpo = fields.Float('Saldo Awal CPO')
    # total_produksi_cpo = fields.Integer('Produksi CPO')
    total_produksi_cpo = fields.Float('Produksi CPO')

    # total_stock_kernel = fields.Integer('Total Stock Kernel')
    total_stock_kernel = fields.Float('Total Stock Kernel')
    # total_pengiriman_kernel = fields.Integer('Total Pengiriman Kernel')
    total_pengiriman_kernel = fields.Float('Total Pengiriman Kernel')
    # saldo_awal_kernel = fields.Integer('Total Stock Kernel kemarin (saldo awal)')
    saldo_awal_kernel = fields.Float('Total Stock Kernel kemarin (saldo awal)')
    # total_produksi_kernel = fields.Integer('Total Produksi Kernel hari ini')
    total_produksi_kernel = fields.Float('Total Produksi Kernel hari ini')

    @api.multi
    def action_approve(self):
        for sounding in self:
            sounding.state='approved'

    @api.onchange('saldo_awal_cpo', 'total_pengiriman_cpo', 'total_cpo_tangki')
    def onchange_qty_cpo(self):
        self.total_produksi_cpo = self.total_cpo_tangki - (self.saldo_awal_cpo - self.total_pengiriman_cpo)

    @api.onchange('saldo_awal_kernel', 'total_pengiriman_kernel', 'total_stock_kernel')
    def onchange_qty_kernel(self):
        self.total_produksi_kernel = self.total_stock_kernel - (self.saldo_awal_kernel - self.total_pengiriman_kernel)



class MillLhpTbs(models.Model):
    _name = "mill.lhp.tbs.line"
    _description = "Laporan Harian Produksi TBS"

    sequence = fields.Integer()
    lhp_id = fields.Many2one('mill.lhp')
    name = fields.Char('Description')
    brutto = fields.Float('Brutto')
    netto = fields.Float('Netto')
    uom_id = fields.Many2one('product.uom', string='UoM')
    type = fields.Selection([('total','total'),('normal','normal')], string='Type')

class MillLhpCpo(models.Model):
    _name = "mill.lhp.cpo.line"
    _description = "Laporan Harian Produksi CPO"

    sequence = fields.Integer()
    lhp_id = fields.Many2one('mill.lhp')
    name = fields.Char('Description')
    storage_id = fields.Many2one('mill.storage')
    height = fields.Float('Ketinggian', digits=0)
    temperature = fields.Float('Suhu/Temperature')
    uom_height_id = fields.Many2one('product.uom', string='UoM')
    uom_temperature_id = fields.Many2one('product.uom', string='UoM')
    type = fields.Selection([('cm','cm'),('mm','mm'),('total','total')], string='Type')
    density = fields.Float('Density', digits=dp.get_precision('Density'))
    volume_liter = fields.Float('Volume Liter')
    uom_volume_liter_id = fields.Many2one('product.uom', string='UoM')
    koreksi_suhu = fields.Float('Faktor Koreksi', digits=dp.get_precision('Koreksi Suhu'))
    jumlah_setelah_koreksi = fields.Float()
    jumlah = fields.Float()
    uom_jumlah_id = fields.Many2one('product.uom', string='UoM')

class MillLhpKernel(models.Model):
    _name = "mill.lhp.kernel.line"
    _description = "Laporan Harian Produksi Kernel"

    sequence = fields.Integer()
    lhp_id = fields.Many2one('mill.lhp')
    name = fields.Char('Description')
    storage_id = fields.Many2one('mill.storage')
    height = fields.Float('Ketinggian', digits=(15,0))
    sample_height = fields.Float('Sample', digits=(15,0))
    real_height = fields.Float('Tinggi Bersih', digits=(15,0))
    desc_1 = fields.Char('Ket. 1')
    type = fields.Selection([('detail','detail'),('total','total'),('bunker','bunker')], string='Type')
    kg_cm = fields.Float('kg/cm')
    desc_2 = fields.Char('Ket. 2')
    density = fields.Float('Densitas', digits=dp.get_precision('Mill Bunker Density'))
    jumlah = fields.Float()
    desc_3 = fields.Char('Ket. 3')
