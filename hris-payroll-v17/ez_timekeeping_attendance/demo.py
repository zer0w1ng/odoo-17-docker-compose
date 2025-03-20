from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.addons.ez_sql import execute_insert
from odoo.addons.ez_sql import execute_insert
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random,time,logging
_logger=logging.getLogger(__name__)
class Attendance(models.Model):
	_inherit='hr.attendance'
	@api.model
	def create_demo_data(self,months=24):
		E=months;B=self;A=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=E);H=A+relativedelta(months=E+1,days=-1);I=B.env['hr.employee'].search([]);J=B.env['ez.time.card'].TIMEZONE_ADJUSTMENT();D=[]
		while A<=H:
			for K in I:
				F=1
				if A.weekday()==6:F=random.randrange(1,31)
				if F==1:
					C=datetime.combine(A,datetime.min.time()).replace(hour=8,minute=0);C-=J;G=C+relativedelta(hours=9);L=random.randrange(1,6)
					if L==1:C+=relativedelta(minutes=random.randrange(1,20))
					M=random.randrange(1,6)
					if M==1:G+=relativedelta(minutes=random.randrange(10,120))
					N={'employee_id':K.id,'check_in':C,'check_out':G};D.append(N)
			A+=relativedelta(days=1)
		if D:B.env.cr.execute('DELETE FROM hr_attendance');execute_insert(B,D,fast_mode=True)
class TimeCard(models.Model):
	_inherit='ez.time.card'
	@api.model
	def create_demo_data(self,months=24):
		F=months;B=self;B.env.cr.execute('DELETE FROM ez_time_card');B.env['ez.time.card'].invalidate_recordset();B.env.cr.execute('DELETE FROM ez_time_record');B.env['ez.time.record'].invalidate_recordset();G=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=F);H=G+relativedelta(months=F+1,days=-1);I=B.env['hr.employee'].search([]);K=B.env['ez.time.card'].TIMEZONE_ADJUSTMENT();D=[]
		for A in I:
			C=G
			while C<=H:D.append({'employee_id':A.id,'date1':C,'date2':C+relativedelta(days=14),'note':'Demo Time Card1','state':'draft','shift_id':A.shift_id.id,'auto_auth':A.shift_id.auto_auth,'flex_time':A.shift_id.flex_time,'minimum_ot_minutes':A.shift_id.minimum_ot_minutes,'late_allowance_minutes':A.shift_id.late_allowance_minutes});D.append({'employee_id':A.id,'date1':C+relativedelta(days=15),'date2':C+relativedelta(months=1,days=-1),'note':'Demo Time Card2','state':'draft','shift_id':A.shift_id.id,'auto_auth':A.shift_id.auto_auth,'flex_time':A.shift_id.flex_time,'minimum_ot_minutes':A.shift_id.minimum_ot_minutes,'late_allowance_minutes':A.shift_id.late_allowance_minutes});C+=relativedelta(months=1)
		if D:execute_insert(B.env['ez.time.card'],D,fast_mode=True)
		E=B.env['ez.time.card'].search([]);E._name_compute()
		for J in E:J.gen_default_lines()
		E.fill_from_attendance(summarized=False);E.approve_record()