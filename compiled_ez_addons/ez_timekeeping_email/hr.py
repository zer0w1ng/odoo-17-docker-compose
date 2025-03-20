from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
import logging,re
_logger=logging.getLogger(__name__)
class HrEmployeeBase(models.AbstractModel):
	_inherit='hr.employee.base';approver_email=fields.Char('Approver E-mail')
	@api.onchange('approver_email')
	def validate_mail(self):
		if self.approver_email:
			A=re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$',self.approver_email)
			if A==None:raise ValidationError('Not a valid E-mail address.')