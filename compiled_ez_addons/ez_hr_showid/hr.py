from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random,logging
_logger=logging.getLogger(__name__)
class HrEmployee(models.Model):
	_inherit='hr.employee'
	@api.depends('name','identification_id')
	def _compute_display_name(self):
		for A in self:
			B=A.sudo().identification_id
			if B:A.display_name='%s [%s]'%(A.name,B)
			else:A.display_name=A.name