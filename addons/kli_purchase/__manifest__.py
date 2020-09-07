# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2020  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Hendra Saputra <hendrasaputra0501@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

{
    'name'      : "Purchase Module for PT. Kalirejo Lestari",
    'category'  : 'Custom Module',
    'version'   : '1.0.0.1',
    'author'    : "Konsaltén Indonesia (Consult10 Indonesia)",
    'website'   : "www.consult10indonesia.com",
    'license'   : 'AGPL-3',
    'depends'   : ['base', 'c10i_base', 'kli_base', 'stock', 'c10i_purchase', 'c10i_purchase_request'],
    'summary'   : """
                        KLI Purchase Module - C10i
                    """,
    'description'   : """
Customize Modul Base KLI
========================

Preferences
-----------
* Add SKB
                    """,
    'data'      : [
        'views/purchase_request_views.xml',
        'views/purchase_views.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
