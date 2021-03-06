# -*- coding: utf-8 -*-
{
    'name': "efecto_dashboard_emdi",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        EMDI Dashboard 
    """,

    'author': "Desarrollado por Efecto Negocio",
    'website': "https://efectonegocio.com/odoo/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale',
                'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_dashboard.xml',
        'views/dashboard_emdi.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
