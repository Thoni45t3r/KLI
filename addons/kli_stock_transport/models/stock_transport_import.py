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
import os, base64, xlrd
import logging
_logger = logging.getLogger(__name__)

class StockTransportIMport(models.Model):
    _name = "stock.transport.import"
    _description = "Transport Import"

    date = fields.Date('Date', required=True)
    file = fields.Binary('File')
    file_name = fields.Char(required=True)
    import_line = fields.One2many('stock.transport.import.line', 'import_id', string='Import Lines', ondelete='cascade')
    state = fields.Selection([('draft','Draft'),('imported','Imported'),('confirmed','Confirmed')], string='State', default='draft')
    keterangan = fields.Text()

    @api.multi
    def validate(self):
        warning = ''
        data = []
        for record in self:
            for line in record.import_line:
                # Transporter
                transporter = self.env['res.partner'].search([('name','=',line.transporter)])
                if not transporter:
                    warning += "Transporter '%s' tidak ada di sistem\n" % (line.transporter)

                # Product
                product = self.env['product.product'].search([('name','=',line.product)])
                if not product:
                    warning += "Product '%s' tidak ada di sistem\n" % (line.product)

                # Source Location
                src_location = self.env['stock.transport.location'].search([('name','=',line.src_location)])
                if not src_location:
                    warning += "Lokasi '%s' tidak ada di sistem\n" % (line.src_location)

                # Destination Location
                dest_location = self.env['stock.transport.location'].search([('name','=',line.dest_location)])
                if not dest_location:
                    warning += "Lokasi '%s' tidak ada di sistem\n" % (line.dest_location)

                # Rate Type
                list_rate_type = dict(self.env['stock.transport.move']._fields['rate_type'].selection)
                rate_type = {k:v for v, k in list_rate_type.items() if k == line.rate_type}
                if not rate_type:
                    warning += "Rate Type '%s' tidak ada dalam opsi" % (line.rate_type)
                else:
                    rate_type = rate_type[line.rate_type]

                if not warning:
                    rate = self.env['stock.transport.rate'].search([
                        ('partner_id', '=', transporter.id),
                        ('product_id', '=', product.id),
                        ('start_date', '<=', line.date),
                        ('end_date', '>=', line.date),
                        ('src_location_id', '=', src_location.id),
                        ('dest_location_id', '=', dest_location.id),
                        ('rate_type', '=', rate_type)
                        ])
                    if not rate:
                        warning += 'Rate Vendor %s, Product %s, Tanggal %s, Lokasi %s, Tujuan %s, Rate Type %s tidak ditemukan\n' % (
                            transporter.name, 
                            product.name,
                            line.date, 
                            src_location.name, dest_location.name, rate_type)
                    else:
                        data.append({
                            'date' : line.date,
                            'transporter' : transporter.id,
                            'product' : product.id,
                            'src_location' : src_location.id,
                            'dest_location' : dest_location.id,
                            'rate_type' : rate_type,
                            'product_qty' : line.product_qty,
                            'price_unit': rate.rate
                            })

            if not warning:
                for item in data:
                    self.env['stock.transport.move'].create({
                        'date' : item.get('date',False),
                        'partner_id' : item.get('transporter',False),
                        'product_id' : item.get('product',False),
                        'src_location_id' : item.get('src_location',False),
                        'dest_location_id' : item.get('dest_location',False),
                        'rate_type' : item.get('rate_type',False),
                        'product_qty' : item.get('product_qty',False),
                        'price_unit' : item.get('price_unit',False),
                        })
                self.write({'state': 'confirmed','keterangan':False})

            else:
                self.write({'keterangan': warning})

    @api.multi
    def action_draft(self):
        for record in self:
            record.state='draft'

    @api.multi
    def import_transport(self):
        return self.upload_import_transport_function(False,False)

    @api.multi
    def upload_import_transport_function(self, workbook, sheet_number):
        data_matrix = {}

        if not workbook and not sheet_number:
            file = os.path.splitext(self.file_name)
            if file[1] not in ('.xls', '.xlsx'):
                raise UserError("Invalid File! Please import the correct file")

            wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
            sheet = wb.sheet_by_index(0)
        else:
            wb = workbook
            sheet = wb.sheet_by_index(sheet_number)

        col = 1
        row = 1

        warning = ''

        # end of header section
        data_matrix = []
        # start validating detail section
        product_template_id = False
        print sheet.cell(0, 1).value,"<<<<<<<<<<<<"
        while row != sheet.nrows:
            _logger.warning("row %s/%s" % (row,sheet.nrows))
            date = False
            transporter = False
            product = False
            src_location = False
            dest_location = False
            rate_type = False
            product_qty = False
            col = 0
            if sheet.cell(row, col).value:
                if sheet.cell_type(row, col) != 3:
                    warning+="Data Kolom Tanggal pada baris ke %s bukan format tanggal\n" % (row)
                else:
                    date = datetime(*xlrd.xldate_as_tuple(sheet.cell(row, col).value, wb.datemode))
            else:
                warning+="Data Tanggal pada baris ke %s tidak diisi\n" % (row)
                
            col+=1

            if sheet.cell(row, col).value:
                transporter = sheet.cell(row, col).value
            else:
                warning+="Data Transporter pada baris ke %s tidak diisi\n" % (row)
           
            col+=1

            if sheet.cell(row, col).value:
                product = sheet.cell(row, col).value
            else:
                warning+="Data Product pada baris ke %s tidak diisi\n" % (row)
           
            col+=1

            if sheet.cell(row, col).value:
                src_location = sheet.cell(row, col).value
            else:
                warning+="Data Source Location pada baris ke %s tidak diisi\n" % (row)
           
            col+=1

            if sheet.cell(row, col).value:
                dest_location = sheet.cell(row, col).value
            else:
                warning+="Data Destination Location pada baris ke %s tidak diisi\n" % (row)
           
            col+=1

            if sheet.cell(row, col).value:
                rate_type = sheet.cell(row, col).value
            else:
                warning+="Data Rate Type pada baris ke %s tidak diisi\n" % (row)
           
            col+=1

            if sheet.cell(row, col).value:
                if sheet.cell_type(row, col) != 2:
                    warning+="Data Product Qty pada baris ke %s bukan format angka\n" % (row)
                else:
                    product_qty = sheet.cell(row, col).value
            else:
                warning+="Data Product Qty pada baris ke %s tidak diisi\n" % (row)
           
            col+=1
            if not warning:
                data_matrix.append([0,False,{
                    'date' : date,
                    'transporter' : transporter,
                    'product' : product,
                    'src_location' : src_location,
                    'dest_location' : dest_location,
                    'rate_type' : rate_type,
                    'product_qty' : product_qty,
                    }])

            row+=1
        if not warning:
            self.write({'import_line': data_matrix, 'state': 'imported', 'keterangan': False})
        else:
            self.write({'keterangan': warning})

        # end of section detail
    
    
class StockTransportIMportLine(models.Model):
    _name = "stock.transport.import.line"
    _description = "Transport Import Line"

    import_id = fields.Many2one('stock.transport.import')
    date = fields.Date('Date')
    transporter = fields.Char()
    product = fields.Char()
    src_location = fields.Char(string='Asal Lokasi')
    dest_location = fields.Char(string='Tujuan Lokasi')
    rate_type = fields.Char(string='Rate Type')
    product_qty = fields.Float(string='Quantity')
    

   