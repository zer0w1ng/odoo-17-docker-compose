from odoo import api,fields,models,tools,_
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,logging
_logger=logging.getLogger(__name__)
day_type_names={'reg':'Regular','do':'Restday','lh':'Regular Holiday','sh':'Special Holiday','do_lh':'Restday & Regular Holiday','do_sh':'Restday & Special Holiday'}
day_types=[('reg','REG'),('do','RD'),('lh','RH'),('sh','SH'),('do_lh','RHRD'),('do_sh','SHRD')]
class TimeRecordDetail(models.Model):
	_inherit='ez.time.record'
	@api.model
	def summarize_time_record2(self,time_recs,ignore_error=False):
		def C(pdict,trec,salary_rate,salary_rate_period,key,qty):
			A=pdict
			if qty:
				B='%s %s'%(trec.day_type,key);C='%s %s'%(salary_rate,salary_rate_period)
				if B not in A:A[B]={}
				A[B][C]=A[B].get(C,0)+qty
		B={}
		for A in time_recs:
			if not ignore_error and A.timelog and A.timelog[:3]=='ERR':raise ValidationError(_('Cannot continue. There are errors on the time card.'))
			F=self.env['hr.employee'].get_date_salary(A.employee_id,A.date);D=F[0];E=F[1];C(B,A,D,E,'absent',A.absent_minutes);C(B,A,D,E,'late',A.late_minutes);C(B,A,D,E,'undertime',A.undertime_minutes);C(B,A,D,E,'norm',A.norm_minutes);C(B,A,D,E,'norm_night',A.norm_night_minutes);C(B,A,D,E,'ot',A.ot_minutes);C(B,A,D,E,'ot_night',A.ot_night_minutes)
		return B