import ast
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import logging
from . import s3_tool
from odoo.exceptions import UserError
import os
import odoo
import configparser as ConfigParser
import optparse

__author__ = odoo.release.author
__version__ = odoo.release.version

_logger = logging.getLogger(__name__)

ASSETS = ["text/css", "application/javascript", "application/octet-stream"]
from datetime import datetime


class S3Config(models.Model):
	_name = "s3.config"
	_description = "Model For Storing S3 Config Values"

	name = fields.Char(string='Name', help="Amazon S3 Cloud Config name", default=datetime.today().strftime('%Y%m%d') + 'AWS3 Config')
	amazonS3bucket_name = fields.Char(
		string='Bucket Name', help="This allows users to store data in Bucket", compute="_getAWS3", store=True,
		readonly=True)
	amazonS3secretkey = fields.Char(
		string='Secret key', help="Amazon S3 Cloud Connection", readonly=True)
	amazonS3accessKeyId = fields.Char(
		string='Access Key Id', help="Amazon S3 Cloud Connection access key Id", readonly=True)
	bucket_location = fields.Char(
		string='Bucket Location', help="Amazon S3 Bucket Location", readonly=True)
	s3_location_constraint = fields.Char(
		string='Location Constraint', help="Amazon S3 Location Constraint", compute="_getLocationConstraint")
	is_store = fields.Boolean("Is Active", default=False, readonly=True)

	@api.depends('name')
	def _getAWS3(self):
		config = odoo.tools.config
		queue_job_config = {}
		try:
			queue_job_config = config.misc.get("aws3_itms", {})
			res = self.env['s3.config'].sudo().search([], limit=1)

			amazonS3bucket_name = queue_job_config.get("amazons3bucket_name")
			amazonS3secretkey = queue_job_config.get("amazons3secretkey")
			amazonS3accessKeyId = queue_job_config.get("amazons3accesskeyid")
			bucket_location = queue_job_config.get("bucket_location")
			is_store = True

			res.update(
				{'amazonS3bucket_name': amazonS3bucket_name, 'amazonS3secretkey': amazonS3secretkey,
				 'amazonS3accessKeyId': amazonS3accessKeyId, 'bucket_location': bucket_location, 'is_store': is_store})
			_logger.info('AWS3 %s/%s: %s,%s,%s,%s', __author__, __version__, amazonS3bucket_name, amazonS3secretkey,
			             amazonS3accessKeyId, bucket_location)
		except Exception:
			pass

	def _getLocationConstraint(self):
		parameter = " "
		if self.is_store:
			parameter = "s3://%s:%s@%s&s3.%s.amazonaws.com" % (self.amazonS3accessKeyId,
			                                                   self.amazonS3secretkey, self.amazonS3bucket_name,
			                                                   self.bucket_location)
		self.s3_location_constraint = parameter
		result = self.env['ir.config_parameter'].sudo().set_param(
			'ir_attachment.location', parameter)
		return result
