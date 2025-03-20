from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import base64,time,random,logging
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class TimeLog(models.Model):_inherit='ez.time.log';ct108u_id=fields.Many2one('ez.time.log.ct108u','CT108U Import',ondelete='cascade')
class TimeLogCt108u(models.Model):
	_name='ez.time.log.ct108u';_description='CT108U Time Logs';_order='date1 desc, name';company_id=fields.Many2one('res.company',string='Company',default=lambda self:self.env['res.company']._company_default_get('ez.time.log.ct108u'));name=fields.Char();date1=fields.Date('Date From');date2=fields.Date('Date To');dat_file=fields.Binary('Biometric File');filename=fields.Char('Filename');timelog_ids=fields.One2many('ez.time.log','ct108u_id','Time Logs')
	def delete_records(A):A.ensure_one();A.timelog_ids=[(5,)]
	def process_file(A):
		A.ensure_one();F=fields.Date.to_string(A.date1);G=fields.Date.to_string(A.date2);_logger.debug('Process biometric file: dt1=%s dt2=%s',F,G)
		if A.dat_file:
			B=[(5,)];I=base64.b64decode(A.dat_file).decode('utf-8').splitlines()
			for C in I:
				if not(C[:8]=='UDISKLOG'or C[:7]=='No\tMchn'):
					D=C.split('\t')
					if len(D)==7:
						J=D[2];H=D[6].split();E=H[0].replace('/','-');K={'name':E,'time':H[1],'identification_id':J}
						if F<=E and G>=E:B.append((0,0,K))
			_logger.debug('ADD: %s',B);A.timelog_ids=B