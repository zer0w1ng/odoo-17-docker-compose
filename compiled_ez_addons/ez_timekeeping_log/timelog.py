from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.addons.ez_sql import execute_insert
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging,time,random
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class TimeLog(models.Model):
	_name='ez.time.log';_description='Raw Time Logs';_order='name desc, time desc';name=fields.Date('Date');time=fields.Char();identification_id=fields.Char('Employee ID Number');sync_id=fields.Integer('Sync ID');employee_name=fields.Char('Employee Name',compute='compute_employee_name')
	@api.depends('identification_id')
	def compute_employee_name(self):
		for A in self:
			B=self.sudo().env['hr.employee'].search([('identification_id','=',A.identification_id)],limit=1)
			if B:A.employee_name=B.name
			else:A.employee_name='INVALID ID NUMBER'
	@api.model
	def get_last_sync_id(self):
		A=self.search([],order='sync_id desc',limit=1)
		if A:return A[0].sync_id
		else:return 0
	@api.model
	def delete_logs(self,date1,date2):B=date2;A=date1;C=self.search([('name','>=',A),('name','<=',B)]);_logger.debug('delete_logs: date1=%s date2=%s records=%s',A,B,len(C));C.unlink();return True
	@api.model
	def insert_logs(self,logs):
		D=logs;E=time.time();_logger.debug('insert_logs: start len=%s',len(D));A=[]
		for B in D:A.append("(%s,%s,'%s','%s','%s')"%("nextval('ez_time_log_id_seq')",B[0],B[1],B[2],B[3]))
		if A:C='\n                INSERT INTO ez_time_log (\n                    id,\n                    sync_id,\n                    name,\n                    time,\n                    identification_id\n                ) VALUES \n';F=',\n'.join([A for A in A]);C=C+F;_logger.debug('INT multi-create trans: start records=%s sql=%s',len(A),C);self.env.cr.execute(C);_logger.debug('INT multi-create trans: stop1 time=%s',time.time()-E);self.env['ez.time.log'].invalidate_recordset();_logger.debug('INT multi-create trans: stop2 time=%s',time.time()-E)
		return{'msg':'Ok','len':len(D)}
	@api.model
	def gen_demo_logs(self):
		H=self;R=time.time();H.env['ez.time.log'].search([('sync_id','=',-1)]).unlink()
		if 0:B=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=1);F=B+relativedelta(months=1)-relativedelta(days=1)
		else:B=fields.Date.from_string(fields.Date.today()).replace(day=1)-relativedelta(months=1);F=B+relativedelta(months=3)-relativedelta(days=1)
		_logger.debug('gen_demo_logs: %s to %s',B.strftime(DF),F.strftime(DF));K=H.env['hr.employee'].search([]);I={}
		for C in K:
			if C.shift_id:M=C.shift_id.get_schedule(B.strftime(DF),F.strftime(DF));I[C.id]=M
		_logger.debug('gen_demo_logs: scheds=%s',I);J=[];D=B;N=F
		while D<=N:
			for C in K:
				S=D.strftime('%Y-%m-%d');G=I[C.id].get(D.strftime(DF))
				if G and G.schedule and not G.day_off:
					O=G.schedule.replace('-',' ').split(' ');E=0
					for P in O:
						A=datetime.strptime(P,'%H:%M')
						if random.random()<.3:
							if E==0:A=A+relativedelta(minutes=random.randint(-10,25))
							elif E==1:A=A+relativedelta(minutes=random.randint(0,15))
							elif E==2:A=A+relativedelta(minutes=random.randint(-15,0))
						if E==3:
							L=random.random()
							if L<.1:A=A+relativedelta(minutes=random.randint(20,120))
							elif L<.15:A=A+relativedelta(minutes=random.randint(-15,10))
						Q={'name':D.strftime(DF),'time':A.strftime('%H:%M'),'identification_id':C.identification_id,'sync_id':-1};J.append(Q);E+=1
			D=D+relativedelta(days=1)
		if J:execute_insert(H,J,fast_mode=True)