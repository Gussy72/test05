# -*- coding: utf-8 -*-
{
    'name': "Dispersion de Pagos",

    'summary': """
        Dispersión de Pagos
     """,

    'description': """
        - Dispersion de pagos Bancomer
    """,

    'author': "appti",
    'website': "http://appti.mx",

    'category': 'report',
    'version': '14.0.0.1',
    'depends': ['account'],

    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/partner_view.xml',
        'views/account_out_invoice_view.xml',
        'views/res_bank_view.xml',
        'wizard/dispersion_view.xml',
    ],
}