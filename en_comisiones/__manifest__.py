# -*- coding: utf-8 -*-
{
    'name': "Administración de Comisiones de Ventas",

    'summary': """
    Configuración de comisiones de ventas.
        
        """,

    'description': """
        Módulo que permite la configuración, registro de ventas y cálculo de comisiones de ventas.
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
        'security/security.xml',
        'views/res_users_commission_views.xml',
        'views/configuracion_comisiones_views.xml',
        'views/sale_order_inherit_views.xml',
        'views/comisiones_pagos_views.xml',
        #'views/dialogo_confirmar.xml',
        'views/prenomina_views.xml',
        #'views/lineas_prenomina_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
