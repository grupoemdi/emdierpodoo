# -*- coding: utf-8 -*-
{
    'name': "Formato SO",

    'summary': """
    Personalizaciones de la SO
        
        """,

    'description': """
        Personalizaciones de la SO
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
                'sale',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'security/security.xml',
        'views/tarifas_cuentas_bancarias.xml',
        'views/report_so_banco.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
