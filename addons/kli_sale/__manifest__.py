# -*- coding: utf-8 -*-
{
    'name'      : "Sale Module for PT. Kalirejo Lestari",
    'category'  : 'Custom Module',
    'version'   : '1.0.0.1',
    'author'    : "Konsaltén Indonesia (Consult10 Indonesia)",
    'website'   : "www.consult10indonesia.com",
    'license'   : 'AGPL-3',
    'depends': ['base', 'c10i_base', 'sale', 'c10i_sale', 'account', 'c10i_account', 'kli_base', 'c10i_document_type', 'report_xlsx'],
    'summary'   :
                """         KLI Sale Module - C10i          """,
    'description'   : """

    Customize Modul Sale KLI
    ========================
    """,


    'data': [
        'views/sale_views.xml',
    ],

    'installable': True,
    'application': True,
}