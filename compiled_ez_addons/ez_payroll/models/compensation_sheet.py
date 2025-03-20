from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging,xlrd,base64,re
from io import BytesIO
_logger=logging.getLogger(__name__)
DEBUG=0
def dprint(s):_logger.debug(s)
class WorkSummary(models.Model):
	_name='ez.work.summary.sheet';_description='Work Summary Sheet';_inherit=['mail.thread'];_order='date desc, name asc'
	def copy(A,default=None):B=default;A.ensure_one();B=dict(B or{},name=_('%s (copy)')%A.name);return super(WorkSummary,A).copy(B)
	def unlink(A):
		for B in A:
			if B.state=='done':raise ValidationError(_('You cannot delete a done compensation sheet.'))
		return super(WorkSummary,A).unlink()
	def set_as_done(A):
		for B in A:B.state='done'
	def cancel_done(A):
		for B in A:B.state='draft'
	@api.model
	def get_pay_lines(self,payslip,work_sheet_ids):
		D=payslip;E=self.env['ez.work.summary.line'].search([('employee_id','=',D.employee_id.id),('qty','!=',.0),('payslip_id','=',False),('work_summary_sheet_id','in',work_sheet_ids)]);B={}
		for A in E:
			C='%s %s %0.6f %s %s'%(A.name,A.unit,A.factor,A.basic_pay,A.taxable)
			if C in B:B[C]['qty']+=A.qty
			else:B[C]={'payslip_id':D.id,'name':A.name,'seq':A.work_type_id.seq,'computed':True,'qty':A.qty,'unit':A.unit,'factor':A.factor,'basic_pay':A.basic_pay,'taxable':A.taxable,'ws_lines':[]}
			B[C]['ws_lines'].append(A.id)
		return B
	@api.model
	def XXcreate_pay_line(self,payslip,work_sheet_ids):
		F=work_sheet_ids;C=payslip;dprint('***CREATE PAY LINE %s'%F);I=C.payroll_id.date_from;J=C.payroll_id.date_to;E=self.env['ez.work.summary.line'].search([('employee_id','=',C.employee_id.id),('qty','!=',.0),('pay_computation_id','=',False),('work_summary_sheet_id','in',F)]);B={}
		for A in E:
			D='%s %s %0.6f %s %s'%(A.name,A.unit,A.factor,A.basic_pay,A.taxable)
			if D in B:B[D]['qty']+=A.qty
			else:B[D]={'payslip_id':C.id,'name':A.name,'seq':A.work_type_id.seq,'computed':True,'qty':A.qty,'unit':A.unit,'factor':A.factor,'basic_pay':A.basic_pay,'taxable':A.taxable,'ws_lines':[]}
			B[D]['ws_lines'].append(A)
		for G in B:
			E=B[G].pop('ws_lines',[]);H=C.pay_computation_line.create(B[G])
			for A in E:A.pay_computation_id=H.id
	company_id=fields.Many2one('res.company',string='Company',default=lambda self:self.env.company);date=fields.Date('Date',default=fields.Date.context_today,required=True);name=fields.Char('Name',required=True);work_type_group_id=fields.Many2one('ez.work.type.group','Type Group',default=lambda self:self.env.ref('ez_payroll.wtg_default'),required=True,ondelete='restrict');note=fields.Text('Notes',readonly=False);default_work_type_id=fields.Many2one('ez.work.type','Work Type',default=lambda self:self.env.ref('ez_payroll.wt_reg_norm').id,required=True,ondelete='restrict');default_unit=fields.Selection([('day','days'),('hour','hours'),('minute','minutes'),('month','month'),('piece','pieces'),('fixed','fixed rate')],string='Unit',required=True,default='day');default_qty=fields.Float('Quantity',default=1,digits='Payslip Line Unit');xls_file=fields.Binary(string='Excel File');filename=fields.Char();work_summary_line=fields.One2many('ez.work.summary.line','work_summary_sheet_id','Compensation Sheet Detail',copy=True);state=fields.Selection([('draft','Draft'),('done','Done')],'State',tracking=True,required=True,default='draft')
	def add_bulk_lines(A):
		A.ensure_one();D=A.env['hr.employee'].search([('company_id','=',A.company_id.id),('exclude_from_payroll','=',False)]);B=[];C=0
		for E in D:C+=10;B.append([0,0,{'seq':C,'work_summary_sheet_id':A.id,'employee_id':E.id,'name':A.default_work_type_id.name,'work_type_id':A.default_work_type_id.id,'unit':A.default_unit,'factor':A.default_work_type_id.factor,'basic_pay':A.default_work_type_id.basic_pay,'taxable':A.default_work_type_id.taxable,'qty':A.default_qty}])
		A.work_summary_line.unlink();A.work_summary_line=B
	def import_excel(A):
		A.ensure_one();A.work_summary_line.unlink();L=base64.b64decode(A.xls_file);M=BytesIO(L)
		try:N=xlrd.open_workbook(file_contents=M.getvalue())
		except:raise ValidationError(_('Wrong excel format.'))
		E=N.sheet_by_index(0);O=[A.value for A in E.row(0)];_logger.debug('Import excel %s',O);H=0
		for F in range(1,E.nrows):
			B=E.row(F);_logger.debug('Row %s: %s',F,B);C='%s'%(B[1].value or'');C=C.strip();D='%s'%(B[2].value or'');D=D.strip()
			if C and D:
				G=A.env['hr.employee'].search([('name','=ilike','%s%%'%C)],limit=1);I=A.env['ez.work.type'].search([('name','=ilike','%s%%'%D),('work_type_group_id','=',A.work_type_group_id.id)],limit=1)
				if G and I:
					J=int(B[0].value or 0)
					if J:H=J
					if B[3].value:P=True
					else:P=False
					K={'work_summary_sheet_id':A.id,'seq':H,'employee_id':G[0].id,'work_type_id':I[0].id,'qty':round(B[3].value or .0,4),'unit':B[4].value};G=A.work_summary_line.create(K);_logger.debug('Val %s: %s',F,K)
		A.work_summary_line.work_type_id_changed()
class WorkSummaryLine(models.Model):
	_name='ez.work.summary.line';_description='Compensation Sheet Lines';_inherit='hr.ph.payslip.line.template';_order='seq'
	@api.onchange('work_type_id')
	def work_type_id_changed(self):
		for A in self:A.name=A.work_type_id.name;A.factor=A.work_type_id.factor;A.basic_pay=A.work_type_id.basic_pay;A.taxable=A.work_type_id.taxable
	seq=fields.Integer(string='Seq',help='Sequence or sorting order.',default=10,index=True);date=fields.Date('Date',related='work_summary_sheet_id.date');work_summary_sheet_id=fields.Many2one('ez.work.summary.sheet','Work Summary Sheet',ondelete='cascade',index=True);employee_id=fields.Many2one('hr.employee','Employee Name',required=True,ondelete='restrict',index=True);work_type_id=fields.Many2one('ez.work.type','Work Type',required=True,ondelete='restrict');payslip_id=fields.Many2one('hr.ph.payslip','Payslip',readonly=True,ondelete='set null',copy=False,index=True);payroll_name=fields.Char(related='payslip_id.payroll_id.name',string='Payroll No.')
	@api.model
	def default_get(self,fields_list):
		A=super(WorkSummaryLine,self).default_get(fields_list);B=dict(self.env.context);D=B.get('default_work_type_id')
		if D:A.update(work_type_id=D)
		C=B.get('default_qty')
		if C:A.update(qty=C)
		F=B.get('default_unit')
		if C:A.update(unit=F)
		E=B.get('work_summary_line')
		if E:A.update(seq=len(E)*10+10)
		return A