# -*- coding: utf-8 -*-
{
    'name': "Entregas Personalizaciones",

    'summary': """
    Personalizaciones en la funcionalidad de entregas
        
        """,

    'description': """
        Personalizaciones en la funcionalidad de entregas
    """,

    'author': "Soluciones 4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale_stock',
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_view_mods.xml',
        'views/causa_cambio_views.xml',
        'views/mail_template_cambio_fecha.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
