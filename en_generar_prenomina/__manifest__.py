# -*- coding: utf-8 -*-
{
    'name': "Generar prenómina",

    'summary': """
        Tarea planificada para generar prenomina
        """,

    'description': """
        Tarea planificada para generar prenómina
    """,

    'author': "Soluciones4G",
    'website': "http://soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','en_comisiones'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/action_view_exec.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}