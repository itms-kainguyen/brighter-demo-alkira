{
    "name": " ITMS - CRM Extended",
    "summary": """

        """,
    "description": """

    """,
    "author": "ITMS Group",
    "website": "https://itmsgroup.com.au",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "crm", "sale", "sale_crm"],
    # always loaded
    "data": [
        'views/crm_lead_view_inherit.xml',
    ],
    "installable": True,
    "application": True,
}
