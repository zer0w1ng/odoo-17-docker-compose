from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
import time,logging
_logger=logging.getLogger(__name__)
DEBUG=0
day_type_names={'reg':'Regular','do':'Restday','lh':'Regular Holiday','sh':'Special Holiday','do_lh':'Restday & Regular Holiday','do_sh':'Restday & Special Holiday'}
day_types=[('reg','REG'),('do','RD'),('lh','RH'),('sh','SH'),('do_lh','RHRD'),('do_sh','SHRD')]
def dprint(s):_logger.debug(s)
def get_dhm(minutes):
	A=minutes
	if A:B=A%480;D=(A-B)/480;C=B%60;E=(B-C)/60;return D,E,C
	else:return 0,0,0
class PayslipInherit(models.Model):
	_inherit='hr.ph.payslip'
	@api.model
	def custom_compensation(self,payslip_id,val):
		if payslip_id.salary_rate_period=='monthly':
			if val['name']=='Special Holiday Work':val['factor']=.3
	@api.model
	def get_compensation_lines(self):A=super(PayslipInherit,self).get_compensation_lines();B=self.get_timecard_compensation_lines();return A+B
	@api.model
	def get_timecard_compensation_lines(self):
		B=self;W=time.time();M=[];N=[];F=['norm','norm_night','ot','ot_night'];O={}
		for X in day_types:
			G=X[0]
			for P in F:C='%s_%s'%(G,P);O[C]=B.env.ref('ez_payroll.wt_%s'%C)
		for P in['absent','late','undertime']:C='reg_%s'%P;O[C]=B.env.ref('ez_payroll.wt_%s'%C)
		for A in B:
			if A.payroll_id.is_13th_month:continue
			J=B.env['ez.time.record'].search([('employee_id','=',A.employee_id.id),('state','=','approved'),('date','>=',A.date_from),('date','<=',A.date_to)]);R=False
			if A.salary_rate_period!='monthly':
				K=0;S='x';Q=False
				for D in J:
					if Q and D.day_type=='reg':
						Q=False
						if not D.timelog:K-=1
					if D.day_type in['lh','do_lh']and not D.timelog:
						if S:_logger.debug('HOL: prev empty');K+=1;Q=True
					if D.day_type=='reg':S=D.timelog
				if K:E={'payslip_id':A.id,'seq':500,'name':'Regular Holiday Paid','computed':True,'qty':K,'unit':'day','factor':1.,'basic_pay':False,'taxable':True};B.custom_compensation(A,E);R=True;M.append(E)
			a={};Y=J.summarize_time_record(J);T=0
			for Z in day_types:
				G=Z[0];H=Y.get(G)
				if H:
					if G=='reg':
						if A.salary_rate_period=='monthly':F=['norm_night','absent','late','undertime','ot','ot_night']
						else:
							U=H.get('norm_night')
							if U:H['norm']=H.get('norm',0)+U
							F=['norm','norm_night','ot','ot_night']
					else:F=['norm','norm_night','ot','ot_night']
					for C in F:
						L=H.get(C);I=O['%s_%s'%(G,C)]
						if L:
							T+=10;E={'payslip_id':A.id,'seq':T,'name':I.name,'computed':True,'factor':I.factor,'basic_pay':I.basic_pay,'taxable':I.taxable};B.custom_compensation(A,E)
							if L>=60:E.update({'qty':L/6e1,'unit':'hour'})
							else:E.update({'qty':L,'unit':'minute'})
							_logger.debug('dtr payslip compute: %s f=%s',E,I.factor);R=True;M.append(E)
			if 1:
				for D in J:N.append(B.env.cr.mogrify('(%s,%s)',(D.id,A.id)).decode('utf-8'))
		if N:V="\n                UPDATE ez_time_record AS t SET\n                    payslip_id = c.payslip_id,\n                    write_uid = %s,\n                    write_date = NOW() at time zone 'UTC'\n                FROM (\n                    VALUES %s\n                ) AS c(id, payslip_id)\n                WHERE c.id = t.id;\n            "%(B.env.uid,','.join(N));_logger.debug('update sql: %s',V);B.env.cr.execute(V);B.env['ez.time.record'].invalidate_recordset()
		_logger.debug('timekeeping get_compensation_lines: %s',time.time()-W);return M