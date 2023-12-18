{
    "name": "Ultimate List View",
    "version": "16.0.1.0",
    "summary": "Ultimate List View",
    "sequence": 30,
    "description": """
        Ultimate List View enables users to filter records in the list view directly from the header of the table in the list view
    """,
    "author": "Zehntech Technologies Inc.",
    "company": "Zehntech Technologies Inc.",
    "contributor": "Zehntech Technologies Inc.",
    "maintainer": "Zehntech Technologies Inc.",
    "website": "https://www.zehntech.com/",
    "support": "odoo-support@zehntech.com",
    "depends": [
        "base",
        "account",
        "crm",
        "web",
        "crm_iap_mine",
        "purchase"
    ],
    "data": [
        "views/pdf.xml",
        "views/pdf_group_by_template.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ultimate_list_view/static/src/xml/dynamic_filter.xml",
            "ultimate_list_view/static/src/css/dynamic_filters.css",
            "ultimate_list_view/static/src/js/dynamic_filter.js",
            "ultimate_list_view/static/src/js/copy_button.js",
            "ultimate_list_view/static/src/views/pdf_export.js",
            "ultimate_list_view/static/src/views/list_button_view.xml",
        ]
    },
    "images": [
        "static/description/banner.gif",
    ],
    "license": "OPL-1",
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 105.00,
    "currency": "USD",
}
