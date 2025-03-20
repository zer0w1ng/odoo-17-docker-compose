from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class Company(models.Model):_inherit='res.company';hdmf_number=fields.Char('HDMF No.');hdmf_signatory=fields.Char('HDMF Signatory')
class HdmfEr2(models.Model):
	_name='ez.hdmf.er2';_description='HDMF ER2';_inherit=['mail.thread'];_order='date desc'
	def default_company_name(A):return A.env.company.name
	def default_company_address(C):
		A=C.env.company;B=A.street or''
		if A.street2:B+=', '+A.street2
		if A.city:B+=', '+A.city
		if A.zip:B+=' '+A.zip
		if A.country_id:B+=' '+A.country_id.name
		return B
	def default_hdmf_number(A):return A.env.company.hdmf_number
	def default_company_email(A):return A.env.company.email
	def default_signatory(A):return A.env.company.hdmf_signatory
	company_id=fields.Many2one('res.company',string='Company',readonly=True,default=lambda self:self.env['res.company']._company_default_get('ez.hdmf.er2'));name=fields.Char(tracking=True,readonly=True,states={'draft':[('readonly',False)]});date=fields.Date('Date',default=fields.Date.today,tracking=True,required=True,readonly=True,states={'draft':[('readonly',False)]});employer_name=fields.Char(tracking=True,default=default_company_name,readonly=True,states={'draft':[('readonly',False)]});employer_number=fields.Char(tracking=True,default=default_hdmf_number,readonly=True,states={'draft':[('readonly',False)]});employer_address=fields.Char(tracking=True,default=default_company_address,readonly=True,states={'draft':[('readonly',False)]});employer_email=fields.Char(tracking=True,default=default_company_email,readonly=True,states={'draft':[('readonly',False)]});signatory=fields.Char(tracking=True,default=default_signatory,readonly=True,states={'draft':[('readonly',False)]});is_initial_list=fields.Boolean('Initial List',tracking=True,readonly=True,states={'draft':[('readonly',False)]});is_subseq_list=fields.Boolean('Subseq. List',tracking=True,readonly=True,states={'draft':[('readonly',False)]});url_er2=fields.Char('Form ER2',compute='_get_url_er2');state=fields.Selection([('draft','Draft'),('done','Done')],string='State',default='draft',tracking=True,required=True);hdmf_er2_line_ids=fields.One2many('ez.hdmf.er2.line','hdmf_er2_id','HDMF ER2 Lines',copy=True,readonly=True,states={'draft':[('readonly',False)]})
	def _get_url_er2(A):
		C=A.env['ir.config_parameter'].sudo().get_param('web.base.url')
		for B in A:B.url_er2='%s/hdmf_er2/%s/er2.pdf'%(C,B.id)
	def set_as_done(A):A.ensure_one();A.state='done'
	def cancel_done(A):A.ensure_one();A.state='draft'
	def get_all_employees(A):
		A.ensure_one();B=set()
		for C in A.hdmf_er2_line_ids:B.add(C.employee_id.id)
		A.add_employees(B)
	def get_new_employees(A):
		A.ensure_one();B=set();C=A.env['ez.hdmf.er2'].search([('state','=','done')])
		for D in C:
			for E in D.hdmf_er2_line_ids:B.add(E.employee_id.id)
		A.add_employees(B)
	def add_employees(B,present_employees):
		F=B.env['hr.employee'].search([]);C=[];D=0
		for A in F:
			if A.id not in present_employees:
				D+=10
				if A.salary_rate_period=='monthly':E=A.salary_rate
				else:E=A.salary_rate*A.emr_days/12.
				G={'hdmf_er2_id':B.id,'seq':D,'employee_id':A.id,'position':A.job_title,'hdmf_number':A.phic_no or A.sss_no,'salary':E,'hired':A.hired};C.append((0,0,G))
		if C:B.write({'hdmf_er2_line_ids':C})
	def print_er2(A):
		A.ensure_one()
		if A.id:C=A.env['ir.config_parameter'].sudo().get_param('web.base.url');B='hdmf_er2/%s/er2.pdf'%A.id;return{'type':'ir.actions.act_url','url':B,'target':'new'}
class HdmfEr2Details(models.Model):_name='ez.hdmf.er2.line';_description='HDMF ER2 Details';_order='seq';hdmf_er2_id=fields.Many2one('ez.hdmf.er2','HMDF ER2',ondelete='cascade');seq=fields.Integer(string='Sequence',help='Sequence or sorting order.');employee_id=fields.Many2one('hr.employee',string='Employee');position=fields.Char();hdmf_number=fields.Char('PHIC/SSS Number');salary=fields.Float(digits='Payroll Amount');hired=fields.Date();prev_employer=fields.Char('Prev. Employer')