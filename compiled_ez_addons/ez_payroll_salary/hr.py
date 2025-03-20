from odoo import api,fields,models,tools,_
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class EmployeeSalary(models.Model):_name='ez.employee.salary';_description='Employee Salary';_order='date desc';employee_id=fields.Many2one('hr.employee','Employee',index=True,ondelete='cascade');date=fields.Date('Date',index=True,required=True);campaign=fields.Char();salary_rate=fields.Float('Salary Rate',digits='Payroll Amount');salary_rate_period=fields.Selection([('daily','per day'),('monthly','per month')],'Rate Period',required=True);note=fields.Text('Notes')
class HrEmployee(models.Model):
	_inherit='hr.employee';rate_ok=fields.Char(compute='compute_rate_ok');salary_ids=fields.One2many('ez.employee.salary','employee_id','Salary',groups='ez_payroll.group_hr_payroll_user')
	@api.depends('salary_rate','salary_rate_period','salary_ids','salary_ids.salary_rate','salary_ids.salary_rate_period')
	def compute_rate_ok(self):
		for A in self:
			if A.salary_ids:
				B=' SALARY MISMATCH'
				for C in A.salary_ids:
					if C.salary_rate==A.salary_rate and C.salary_rate_period and A.salary_rate_period:B=''
					break
				A.rate_ok=B
			else:A.rate_ok=''
	def add_salary_line(A):
		A.ensure_one();B=fields.Date.today();C=A.env['ez.employee.salary'].search([('employee_id','=',A.id),('date','=',B)]);_logger.debug('Date %s %s: %s',B,A.id,C)
		if C:C[0].write({'salary_rate':A.salary_rate,'salary_rate_period':A.salary_rate_period});E=C[0]
		else:E=A.env['ez.employee.salary'].create({'employee_id':A.id,'date':B,'salary_rate':A.salary_rate,'salary_rate_period':A.salary_rate_period})
		D=A.env['ez.employee.salary'].search([('employee_id','=',A.id),('date','=',B),('id','!=',E.id)])
		if D:_logger.debug('DEL %s',D);D.unlink()
	@api.model
	def get_date_salary(self,employee_id,date):
		A=employee_id;self.env.cr.execute('\n            SELECT salary_rate, salary_rate_period\n            FROM ez_employee_salary\n            WHERE employee_id = %s\n                AND date <= %s\n            ORDER BY date desc\n            LIMIT 1\n        ',(A.id,date));B=self.env.cr.fetchall()
		if B:return B[0][0],B[0][1]
		else:return A.salary_rate,A.salary_rate_period