from odoo import api,fields,models,tools,_
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,logging
_logger=logging.getLogger(__name__)
day_type_names={'reg':'Regular','do':'Restday','lh':'Regular Holiday','sh':'Special Holiday','do_lh':'Restday & Regular Holiday','do_sh':'Restday & Special Holiday'}
day_types=[('reg','REG'),('do','RD'),('lh','RH'),('sh','SH'),('do_lh','RHRD'),('do_sh','SHRD')]
class PayComputation(models.Model):
	_inherit='hr.ph.pay.computation';campaign=fields.Char();salary_rate=fields.Float('Salary',digits='Payroll Amount');salary_rate_period=fields.Selection([('daily','per day'),('monthly','per month')],'Period',default='monthly')
	@api.depends('qty','unit','factor','salary_rate','salary_rate_period','payslip_id','payslip_id.emr_days','payslip_id.year_month','payslip_id.salary_rate','payslip_id.salary_rate_period')
	def _compute_amount(self):
		for A in self:
			A.year_month=A.payslip_id.payroll_id.year_month;C=A.payslip_id.emr_days or 313.
			if A.salary_rate:
				if A.unit=='month':
					if A.salary_rate_period=='monthly':A.amount=A.qty*A.factor*A.salary_rate
					else:A.amount=A.qty*A.factor*A.salary_rate*C/12.
					continue
				if A.salary_rate_period=='monthly':B=A.salary_rate*12./C
				else:B=A.salary_rate
			else:
				if A.unit=='month':
					if A.payslip_id.salary_rate_period=='monthly':A.amount=A.qty*A.factor*A.payslip_id.salary_rate
					else:A.amount=A.qty*A.factor*A.payslip_id.salary_rate*C/12.
					continue
				if A.payslip_id.salary_rate_period=='monthly':B=A.payslip_id.salary_rate*12./C
				else:B=A.payslip_id.salary_rate
			if A.unit=='day':D=B
			elif A.unit=='hour':D=B/8.
			elif A.unit=='minute':D=B/48e1
			else:D=1.
			A.amount=round(A.qty,4)*A.factor*D
class WorkSummary(models.Model):
	_inherit='ez.work.summary.sheet'
	@api.model
	def get_pay_lines(self,payslip,work_sheet_ids):
		D=payslip;H=self.env['ez.work.summary.line'].search([('employee_id','=',D.employee_id.id),('qty','!=',.0),('payslip_id','=',False),('work_summary_sheet_id','in',work_sheet_ids)]);B={}
		for A in H:
			if A.salary_rate:E=A.salary_rate;F=A.salary_rate_period
			else:G=self.env['hr.employee'].get_date_salary(D.employee_id,A.work_summary_sheet_id.date);E=G[0];F=G[1]
			C='%s %s %0.6f %s %s %s %s %s'%(A.name,A.unit,A.factor,A.basic_pay,A.taxable,A.campaign,E,F or'-')
			if C in B:B[C]['qty']+=A.qty
			else:B[C]={'payslip_id':D.id,'name':A.name,'seq':A.work_type_id.seq,'computed':True,'qty':A.qty,'unit':A.unit,'factor':A.factor,'basic_pay':A.basic_pay,'taxable':A.taxable,'campaign':A.campaign or'','salary_rate':E,'salary_rate_period':F,'ws_lines':[]}
			B[C]['ws_lines'].append(A.id)
		return B
class PayslipInherit(models.Model):
	_inherit='hr.ph.payslip'
	@api.model
	def get_timecard_compensation_lines(self):
		B=self;a=time.time();O=[];P=[];I=['norm','norm_night','ot','ot_night'];Q={}
		for b in day_types:
			F=b[0]
			for G in I:C='%s_%s'%(F,G);Q[C]=B.env.ref('ez_payroll.wt_%s'%C)
		for G in['absent','late','undertime']:C='reg_%s'%G;Q[C]=B.env.ref('ez_payroll.wt_%s'%C)
		for A in B:
			if A.payroll_id.is_13th_month:continue
			J=B.env['ez.time.record'].search([('employee_id','=',A.employee_id.id),('state','=','approved'),('date','>=',A.date_from),('date','<=',A.date_to)]);c=False
			if A.salary_rate_period!='monthly':
				K=[];S='x';R=False
				for D in J:
					if R and D.day_type=='reg':
						R=False
						if K and not D.timelog:K.pop()
					if D.day_type in['lh','do_lh']and not D.timelog:
						if S:_logger.debug('HOL: prev empty');K.append(D.date);R=True
					if D.day_type=='reg':S=D.timelog
				E={}
				for d in K:T=B.env['hr.employee'].get_date_salary(A.employee_id,d);E={'payslip_id':A.id,'seq':500,'name':'Regular Holiday Paid','computed':True,'qty':1,'unit':'day','factor':1.,'basic_pay':False,'taxable':True,'salary_rate':T[0],'salary_rate_period':T[1]};B.custom_compensation(A,E);O.append(E)
			i={};H=J.summarize_time_record2(J);U=0
			for e in day_types:
				F=e[0]
				if F=='reg':
					if A.salary_rate_period=='monthly':I=['norm_night','absent','late','undertime','ot','ot_night']
					else:
						V=H.get(F+' norm_night',{})
						for C in V:
							L=F+' norm'
							if L not in H:H[L]={}
							f=V[C];H[L][C]=H[L].get(C,0)+f
						I=['norm','norm_night','ot','ot_night']
				else:I=['norm','norm_night','ot','ot_night']
				for W in I:
					C='%s %s'%(F,W);X=H.get(C,{})
					for G in X:
						Y=G.split(' ');g=float(Y[0]);h=Y[1];M=X[G];N=Q['%s_%s'%(F,W)]
						if M:
							U+=10;E={'payslip_id':A.id,'seq':U,'name':N.name,'computed':True,'factor':N.factor,'basic_pay':N.basic_pay,'taxable':N.taxable,'salary_rate':g,'salary_rate_period':h};B.custom_compensation(A,E)
							if M>=60:E.update({'qty':M/6e1,'unit':'hour'})
							else:E.update({'qty':M,'unit':'minute'})
							_logger.debug('dtr payslip compute: %s'%E);c=True;O.append(E)
			if 1:
				for D in J:P.append(B.env.cr.mogrify('(%s,%s)',(D.id,A.id)).decode('utf-8'))
		if P:Z="\n                UPDATE ez_time_record AS t SET\n                    payslip_id = c.payslip_id,\n                    write_uid = %s,\n                    write_date = NOW() at time zone 'UTC'\n                FROM (\n                    VALUES %s\n                ) AS c(id, payslip_id)\n                WHERE c.id = t.id;\n            "%(B.env.uid,','.join(P));_logger.debug('update sql: %s',Z);B.env.cr.execute(Z);B.env['ez.time.record'].invalidate_recordset()
		_logger.debug('timekeeping get_compensation_lines: %s',time.time()-a);return O