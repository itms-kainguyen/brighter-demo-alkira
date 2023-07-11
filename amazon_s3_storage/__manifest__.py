{
	"name": "Amazon S3 Cloud Storage",
	"summary": """Store your Odoo attachment to Amazon S3 cloud Storage""",
	"description": """Store your Odoo attachment to Amazon S3 Cloud Storage
	  amazon s3 storage
	  amazon s3 bucket storage
	  amazon cloud storage
	  Store odoo attachments on amazon s3 storage
	  sync odoo attachments on amazon s3 bucket
	""",
	"depends": [
		'base_setup',
		'web_tour',
		'website',
	],
	"category": "ITMS/ITMS",
	'author': "ITMS Group",
	'website': "https://itmsgroup.com.au",
	'maintainers': ["son.nguyen"],
	'license': 'LGPL-3',
	"data": [
		'security/ir.model.access.csv',
		'data/default_data.xml',
		'views/base_config_view.xml',
	],
	"images": ['static/description/banner.gif'],
	"application": True,
	"installable": True,
	"external_dependencies": {'python': ['boto3', 'botocore']},
}
