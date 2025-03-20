from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.tools.misc import xlwt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging,base64
from io import BytesIO
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class Payroll(models.Model):
	_inherit='hr.ph.payroll'
	@api.model
	def get_bank_report_data(self,payslip_ids):
		C=self;A=xlwt.easyxf('font: bold on');F=xlwt.easyxf('font: bold on; align: horiz right');G=xlwt.easyxf(num_format_str='#,##0.00');H=xlwt.easyxf('font: bold on',num_format_str='#,##0.00');D=[[('BANK REPORT',A)],[('Payroll No.:',0),(C.name,0)],[('Date Range:',0),(fields.Date.from_string(C.date_from).strftime('%m/%d/%Y to ')+fields.Date.from_string(C.date_to).strftime('%m/%d/%Y'),0)],[],[('ID Number',A),('Last Name',A),('First Name',A),('Middle Initial',A),('Account No.',A),('Amount',F)]];E=5;I=E+1
		for B in payslip_ids:D.append([(B.employee_id.identification_id or'',0),(B.employee_id.last_name or'',0),(B.employee_id.first_name or'',0),(B.employee_id.middle_name and B.employee_id.middle_name[0]or'',0),(B.employee_id.atm_no or'',0),(B.net_pay or .0,G)]);E+=1
		D.append([('',0),('',0),('',0),('',0),('TOTAL:',A),(xlwt.Formula('SUM(F%s:F%s)'%(I,E)),H)]);return D
	def create_bank_report(A,employee_ids=False):
		F=employee_ids;A.ensure_one();filter=[('payroll_id','=',A.id)]
		if F:filter.append(('employee_id','in',F))
		G=A.env['hr.ph.payslip'].search(filter)
		if not G:raise ValidationError(_('No records found.'))
		H=xlwt.Workbook();I=H.add_sheet('Bank Report');B=A.get_bank_report_data(G);D=0
		for J in B:
			E=0
			for C in J:
				if C[1]:I.write(D,E,C[0],C[1])
				else:I.write(D,E,C[0])
				E+=1
			D+=1
		B=BytesIO();H.save(B);K=base64.b64encode(B.getvalue());return K
class BankWizard(models.TransientModel):
	_name='ez.bank.wizard';_description='Bank Wizard'
	def get_default_ym(A):B=fields.Date.context_today(A);C=fields.Date.from_string(B);return C.strftime('%Y-%m')
	company_id=fields.Many2one('res.company',string='Company',default=lambda self:self.env.user.company_id.id);payroll_id=fields.Many2one('hr.ph.payroll',string='Payroll',required=True);employee_ids=fields.Many2many('hr.employee',string='Employees');xls_file=fields.Binary(string='Excel Output File',readonly=True);filename=fields.Char()
	def gen_excel(A):A.ensure_one();B=A.payroll_id.create_bank_report(employee_ids=A.employee_ids.ids);A.write({'xls_file':B,'filename':'bank-report-%s.xls'%A.payroll_id.name});return{'name':'Bank Report','view_type':'form','view_mode':'form','res_model':'ez.bank.wizard','res_id':A.id,'type':'ir.actions.act_window','target':'new','context':A._context.copy()}