from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,logging
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class TimeRecordDetail(models.Model):
	_inherit='ez.time.record'
	def get_time_logs(B,demo=False):
		for A in B:
			if not demo:
				if A.day_type=='reg':A.timelog=False
			elif A.schedule:A.timelog,A.auth_hrs=get_demo_timelog(A.schedule)
class TimeCard(models.Model):
	_inherit='ez.time.card'
	def fill_from_time_logs(A):_logger.debug('fill_from_time_logs');A.ensure_one();A.sudo().fill_time_logs();A.sudo().summarize()
	def del_from_time_logs(A):
		for B in A.sudo():B.details.write({'timelog':False})
		A.sudo().summarize()
	def fill_time_logs(B,demo=False,process_new_records=True):
		F=time.time();I=[];J=[];N=[]
		for C in B:
			K=fields.Date.from_string(C.date2)+relativedelta(days=1);T=B.env['ez.time.log'].search([('name','>=',C.date1),('name','<=',K.strftime(DF)),('identification_id','=',C.employee_id.identification_id)],order='name,time');D={}
			for O in T:
				L=fields.Date.to_string(O.name)
				if L not in D:D[L]=[]
				D[L].append(O.time[:5])
			_logger.debug('logs %s: %s',C.employee_id.name,D)
			for A in C.details:
				if not A.done and not A.timelog:
					F=time.time();P=fields.Date.to_string(A.date);M=D.get(P,[]);K=fields.Date.from_string(A.date)+relativedelta(days=1);Q=D.get(K.strftime(DF),[]);_logger.debug('detail log %s: cday=%s cday2%s',P,M,Q)
					if'N'in A.schedule:
						G=[]
						for H in M:
							if H>'18:00':G.append(H)
						for H in Q:
							if H<='18:00':G.append('N%s'%H)
					else:G=M
					if G:E=' '.join(G)
					else:E=False
					E=C.shift_id.format_schedule(E,error=False)
					if E:I.append("(%s,'%s')"%(A.id,E));J.append((A.id,E))
					else:I.append('(%s,NULL)'%A.id);J.append((A.id,False))
					N.append(A.id);_logger.debug('fill time log: done time=%s',time.time()-F)
		if I:
			if 1:
				for R in J:U=B.env['ez.time.record'].browse(R[0]);U.timelog=R[1]
			else:S="\n                    UPDATE ez_time_record AS t SET\n                        timelog = c.timelog,\n                        write_uid = %s,\n                        write_date = NOW() at time zone 'UTC'\n                    FROM (\n                        VALUES %s\n                    ) AS c(id, timelog)\n                    WHERE c.id = t.id;\n                "%(B.env.uid,','.join(I));_logger.debug('updates sql: %s',S);B.env.cr.execute(S);B.env['ez.time.record'].invalidate_recordset();_logger.debug('sql done %s',time.time()-F)
			V=B.env['ez.time.record'].browse(N);_logger.debug('browse done %s',time.time()-F)
			if process_new_records:V._process_new_records()
			_logger.debug('wt compute done %s',time.time()-F)