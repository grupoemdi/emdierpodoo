# -*- coding: utf-8 -*-
{
    'name': "en_calendar_custom",

    'summary': """
        Calendarios para entregas
        """,

    'description': """
        Calendarios para entregas de concreto
    """,

    'author': "Soluciones 4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','calendar'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/calendar_event_inherit_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
