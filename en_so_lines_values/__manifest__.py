# -*- coding: utf-8 -*-
{
    'name': "en_so_lines_values",

    'summary': """
        Modificaciones en valores de las sale order lines""",

    'description': """
        Modificaciones en los valores de las sale order lines utilizando
        cálculos especificados
    """,

    'author': "Soluciones 4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_mods.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}