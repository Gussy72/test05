# -*- coding: utf-8 -*-
{
    'name': "Partner Addenda",

    'summary': """
        Agregar todas las addendas que se vayan desarrollando
    """,

    'description': """
        Este módulo permite agregar y modificar las addendas
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Uncategorized',

    'version': '14.0.1',

    'depends': ['base','l10n_mx_edi','contacts'],

    'data': [
        'security/addenda_security.xml',
        'security/ir.model.access.csv',

        'views/account_move.xml',
        'views/addenda_casa_ley.xml',
        'views/addenda_chedrahui.xml',
        'views/addenda_farmacias_guadalajara.xml',
        'views/addenda_fresko.xml',
        'views/addenda_heb.xml',
        'views/addenda_smart.xml',
       # 'views/addenda_soriana.xml',
        'views/addenda_walmart_odoo14.xml',
        'views/res_partner_supplierinfo.xml',
        'views/res_partner.xml',
        'views/product_supplierinfo.xml',
    ],

    'demo': [
    ],
}
