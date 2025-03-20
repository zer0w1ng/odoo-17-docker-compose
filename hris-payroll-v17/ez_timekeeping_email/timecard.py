from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import re,logging
_logger=logging.getLogger(__name__)
class TimeRecord(models.Model):
	_inherit='ez.time.record';day_type_name=fields.Char('Day',compute='get_date_type_name')
	@api.depends('day_type')
	def get_date_type_name(self):
		B={'reg':'REG','do':'RD','lh':'RH','sh':'SH','do_lh':'RHRD','do_sh':'SHRD'}
		for A in self:A.day_type_name=B.get(A.day_type,'REG')
class TimeCard(models.Model):
	_inherit='ez.time.card';sender_email=fields.Char('Sender E-mail',compute='get_sender_email');approver_email=fields.Char('Approver E-mail',related='employee_id.approver_email')
	def get_sender_email(A):
		B=A.env['fetchmail.server'].sudo().search([],limit=1).user
		for C in A:C.sender_email=B
	@api.model
	def is_validate_mail(self,email):
		A=email
		if A:
			B=re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$',A)
			if B==None:return False
			return True
		else:return False
	def to_sent(A):
		super(TimeCard,A).to_sent();C=A.env.ref('ez_timekeeping_email.email_approval_template')
		for B in A:
			if B.employee_id.approver_email and B.sender_email and A.is_validate_mail(B.sender_email):C.send_mail(B.id,force_send=True)
	@api.model
	def check_approval_email(self):
		def C(text):
			B=re.sub('<[^>]*>','\n',text).split('\n');C=[]
			for A in B:
				if A.strip():return A
			return''
		D=fields.Date.today()-relativedelta(months=4);E=self.search([('date1','>=',D),('state','=','sent')])
		for A in E:
			F=self.env['mail.message'].search([('id','in',A.message_ids.ids),('subject','ilike','RE: Time Card of'),('date','>',A.write_date)])
			for G in F:
				B=C(G.body).upper()
				if'APPROVE'in B:_logger.debug('APPROVED: %s %s %s %s',A.employee_id.name,A.date1,A.date2,A.state);A.approve_record();break
				elif'DENY'in B or'DENIED'in B:_logger.debug('DENIED: %s %s %s %s',A.employee_id.name,A.date1,A.date2,A.state);A.to_denied();break