# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2018  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Deby Wahyu Kurdian <deby.wahyu.kurdian@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

{
    'name'      : "Base Module for PT. Kalirejo Lestari",
    'category'  : 'Custom',
    'version'   : '1.0.0.1',
    'author'    : "Konsaltén Indonesia (Consult10 Indonesia)",
    'website'   : "www.consult10indonesia.com",
    'license'   : 'AGPL-3',
    'depends'   : ['base', 'c10i_base', 'c10i_document_type', 'c10i_account', 'c10i_account_location', 'c10i_palm_oil_mill','c10i_account_invoice_advance', 'c10i_purchase', 'c10i_sale'],
    'summary'   : """
                        KLI Base Module - C10i
                    """,
    'description'   : """
                        Customize Modul Base KLI.
                    """,
    'data'      : [
        'security/head_office_security.xml',
        'data/ir_config_parameter_background.xml',
        'views/ir_sequence_views.xml',
        'views/res_partner_views.xml',
        'views/res_document_type_views.xml',
        'views/assets.xml',
        'views/mill_views.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
