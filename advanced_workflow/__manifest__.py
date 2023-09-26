# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Advanced Workflow',
    'version': '16.0.1.0.0',
    'live_test_url': 'https://youtu.be/rKxh8lXfdVw',
    'sequence': 1,
    'summary': """Advanced Stepper, Workflow Process, Advanced process, Advanced statusbar, Elegant Stepper, Elegant Workflow, Elegant statusbar, Workflow State, Workflow Status, Workflow Statusbar Odoo Actions,
                Automatic Workflow Settings, Dynamic Workflow Builder, Module Workflows, Workflow Transactions, Auto Workflow Actions, Approval Workflow, Task Workflow Approval, Action Buttons, Take next step,
                Auto Workflow Management, Workflow stepper, Workflow steps, Workflow Transition, Workflow Status bar, Web Responsive Workflow, Web backend Workflow, Web Workflow, Workflow All in One, Task Workflow,
                Workflow Dynamic, Workflow Stateful, State Workflow Mixin, Stateful Workflow, Status bar Workflow, Process Workflow, stepper Workflow, Transfer Workflow, Task Work flow, Tasks Project Workflow, 
                Approve Reject Workflow, Approve Workflow, Reject Workflow, Update Workflow, Validate Workflow, Check Workflow, All in One Workflow, All in One Statusbar, Cancel Workflow, Edit Workflow Odoo,
                Advanced Odoo Workflow, Advanced Odoo Statusbar, Web Responsive Workflow, Advanced Odoo Stepper, Advanced Stepper Actions, Step by Step Process Workflow Process, Web Odoo Backend Workflow Builder,
                Alter Workflow, Workflow stages, Stage, CRM Workflow, HR Workflow, Invoice Workflow, Invoices Workflow, Sales Workflow, Sale Workflow, Purchase Workflow, Accounting Workflow, Odoo Statusbar Advanced,
                Web Odoo Backend Workflow Builder, Odoo Web Workflow Dynamic, Web Backend Workflow, Web Odoo Backend Statusbar Builder, Odoo Web Statusbar Dynamic, Web Statusbar Workflow, Odoo Advanced Statusbar,
                Customization Process, Customization stepper, Customization Statusbar, Customization Actions, Workflow View, Workflow Enhancements, Workflow Design, Workflow Style, CRM Lead Workflow Action Buttons,
                All in One Process, All in One stepper, All in One step, All in One Status bar, All in One Action, Workflow Customization, Workflow Customize, Customization Workflow, Beautiful Stepper""",
    'description': "An incredible workflow for users to handle their process.",
    'author': 'Innoway',
    'maintainer': 'Innoway',
    'price': '15.0',
    'currency': 'EUR',
    'website': 'https://innoway-solutions.com',
    'license': 'OPL-1',
    'images': [
        'static/description/wallpaper.png'
    ],
    'depends': [
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'advanced_workflow/static/src/xml/statusbar.xml',
            'advanced_workflow/static/src/scss/statusbar.scss',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
