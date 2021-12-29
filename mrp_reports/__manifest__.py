# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Reports",

    'summary': """
       Additional Manufacturing Reports
    """,
    'description': """
        Adds Manufacturing reports as:
    1.- Required Materials in selected production orders (level 1) even if out of stock

    """,

    'author': "silvau",
    'website': "http://www.zeval.com.mx",
    'category': 'reports',
    'version': '12.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/mrp_production_templates.xml',
        'report/mrp_report_views_main.xml',
    ],
}
