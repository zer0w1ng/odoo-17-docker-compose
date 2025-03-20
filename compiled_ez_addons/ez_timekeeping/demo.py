from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from datetime import*
from dateutil.relativedelta import*
import logging
_logger=logging.getLogger(__name__)
class Shift(models.Model):_inherit='ez.shift'
class TimeCard(models.Model):
	_inherit='ez.time.card'
	@api.model
	def X_create_demo_record(self,vals):res=super(TimeCard,self).create(vals);res.gen_default_lines();res.summarize();return res
	@api.model
	def demo_add_emp_shift(self):
		s=self.env.ref('ez_timekeeping.day_shift');s.create_details();emps=self.env['hr.employee'].search([('shift_id','=',False)]);_logger.debug('demo_add_emp_shift: %s',len(emps))
		for e in emps:e.shift_id=s.id
	@api.model
	def Xcreate_demo_data(self):
		timecards=self.env['ez.time.card'].search([('note','=','Demo Time Card')]);dd1=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=1);dd2=dd1.replace(day=15);dd3=dd2+relativedelta(days=1);dd4=dd1+relativedelta(months=1,days=-1);de1=fields.Date.from_string(fields.Date.today()).replace(day=1);de2=de1.replace(day=15);de3=de2+relativedelta(days=1);de4=de1+relativedelta(months=1,days=-1);self.env['ez.holiday'].create_holiday_year(str(dd1.year))
		if not timecards:
			emps=self.env['hr.employee'].search([]);trec_ids=[]
			for a in[(dd1,dd2),(dd3,dd4),(de1,de2),(de3,de4)]:
				d1,d2=a;_logger.debug('Create timekeeping demo: %s to %s'%(d1.strftime('%Y-%m-%d'),d2.strftime('%Y-%m-%d')))
				for e in emps:sd1=d1.strftime('%Y-%m-%d');sd2=d2.strftime('%Y-%m-%d');_logger.debug('Create time card for %s %s-%s'%(e.name,sd1,sd2));t=timecards.create({'employee_id':e.id,'date1':sd1,'date2':sd2,'note':'Demo Time Card','shift_id':e.shift_id.id});trec_ids.append(t.id)
			if trec_ids:t=self.env['ez.time.card'].browse(trec_ids);t.gen_default_lines(demo=True);t.summarize();t.approve_record()