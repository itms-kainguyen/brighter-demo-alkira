{
    "name": "General - ITMS",
    "summary": """
        Contain all general extended feature
        """,
    "description": """

    """,
    "author": "ITMS Group",
    "website": "http://www.itmsgroup.com.au",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "ITMS",
    "version": "16.3.1",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "views/res_config_settings.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "itms_general/static/src/**/*",
            # "itms_general/static/src/css/bootstrap.css",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": True,
}
