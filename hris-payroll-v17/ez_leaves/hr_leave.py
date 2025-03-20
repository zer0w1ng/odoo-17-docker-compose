from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
import logging
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class HrLeave(models.Model):
	_inherit='hr.leave';payslip_id=fields.Many2one('hr.ph.payslip','Payslip',readonly=True,ondelete='set null',copy=False);payroll_name=fields.Many2one(related='payslip_id.payroll_id',string='Payroll Link',readonly=True)
	def _validate_leave_request(B):
		super(HrLeave,B)._validate_leave_request();C=B.filtered(lambda hol:hol.holiday_type=='employee')
		for A in C:D=B.sudo().env['ez.time.record'].search([('employee_id','=',A.employee_id.id),('date','>=',A.request_date_from),('date','<=',A.request_date_to)]);D.write({'note':A.holiday_status_id.name})
		return True