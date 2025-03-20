from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
class Payroll(models.Model):_inherit='hr.ph.payroll';no_gmb=fields.Boolean('No SSS, PHIC and HDMF',readonly=True,states={'draft':[('readonly',False)]})
class Sss(models.Model):
	_inherit='hr.ph.sss'
	@api.model
	def create_sss_line(self,payslip,ptotal):
		A=payslip
		if A.payroll_id.no_gmb:return[]
		else:return super(Sss,self).create_sss_line(A,ptotal)
class Phic(models.Model):
	_inherit='hr.ph.phic'
	@api.model
	def create_phic_line(self,payslip,ptotal):
		A=payslip
		if A.payroll_id.no_gmb:return[]
		else:return super(Phic,self).create_phic_line(A,ptotal)
class PayslipDeduction(models.Model):
	_inherit='hr.ph.pay.deduction'
	@api.model
	def create_hdmf_line(self,payslip,ptotal):
		A=payslip
		if A.payroll_id.no_gmb:return[]
		else:return super(PayslipDeduction,self).create_hdmf_line(A,ptotal)