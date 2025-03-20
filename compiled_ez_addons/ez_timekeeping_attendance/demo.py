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
	def create_demo_data(self,months=6):
		G=months;B=self;B.env.cr.execute('DELETE FROM ez_time_card');B.env['ez.time.card'].invalidate_recordset();B.env.cr.execute('DELETE FROM ez_time_record');B.env['ez.time.record'].invalidate_recordset();H=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=G);M=H+relativedelta(months=G+1,days=-1);N=B.env['hr.employee'].search([('exclude_create_timecard','=',False)]);Q=B.env['ez.time.card'].TIMEZONE_ADJUSTMENT();E=[];I=True;J=B.env['ez.time.card']
		for A in N:
			D=H
			while D<=M and A.shift_id:
				_logger.debug('DEMO: %s %s',A.name,A.shift_id.name);K={'employee_id':A.id,'date1':D,'date2':D+relativedelta(days=14),'note':'Demo Time Card1','state':'draft','shift_id':A.shift_id.id,'auto_auth':A.shift_id.auto_auth,'flex_time':A.shift_id.flex_time,'minimum_ot_minutes':A.shift_id.minimum_ot_minutes,'late_allowance_minutes':A.shift_id.late_allowance_minutes};E.append(K);L={'employee_id':A.id,'date1':D+relativedelta(days=15),'date2':D+relativedelta(months=1,days=-1),'note':'Demo Time Card2','state':'draft','shift_id':A.shift_id.id,'auto_auth':A.shift_id.auto_auth,'flex_time':A.shift_id.flex_time,'minimum_ot_minutes':A.shift_id.minimum_ot_minutes,'late_allowance_minutes':A.shift_id.late_allowance_minutes};E.append(L)
				if not I:
					O=J.create(K);P=J.create(L)
					for C in[O,P]:C._name_compute();C.gen_default_lines();C.gen_default_lines();C.fill_from_attendance(summarized=False);C.approve_record()
				D+=relativedelta(months=1)
		if I:
			if E:execute_insert(B.env['ez.time.card'],E,fast_mode=True)
			F=B.env['ez.time.card'].search([]);F._name_compute()
			for C in F:C.gen_default_lines()
			F.fill_from_attendance(summarized=False);F.approve_record()