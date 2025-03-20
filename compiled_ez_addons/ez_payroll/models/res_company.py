from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
import re,logging
_logger=logging.getLogger(__name__)
class Company(models.Model):_inherit='res.company';payslip_header=fields.Char('Payslip Header')
class Partner(models.Model):
	_inherit='res.partner'
	@api.model
	def change_odoo_bot(self):
		G=self.env.ref('base.partner_root')
		if G:G.name='EzBot'
		H=re.compile('(<a.*>Odoo.*</a>)');F=re.compile('Odoo');I=re.compile('OdooBot');J=re.compile('[0-9][+]? million');K=self.env['mail.template'].search([])
		for D in K:
			_logger.debug('TEMPLATE: search %s',D.name);A=D.body_html;E=False;B=re.findall(F,D.subject)
			if B:_logger.debug('odoo subject %s',B);C='EzPayroll';D.subject=F.sub(C,D.subject)
			B=re.findall(H,A)
			if B:_logger.debug('powered %s',B);C='<a target="_blank" href="https://www.eztechsoft.com" style="color: #9db49d;">EzTech Software</a>';A=H.sub(C,A);E=True
			B=re.findall(I,A)
			if B:_logger.debug('odoo-bot %s',B);C='EzBot';A=I.sub(C,A);E=True
			B=re.findall(F,A)
			if B:_logger.debug('odoo %s',B);C='EzPayroll';A=F.sub(C,A);E=True
			B=re.findall(J,A)
			if B:_logger.debug('millon %s',B);C='thousands of';A=J.sub(C,A);E=True
			if E:_logger.debug('Changed: search %s',A);D.body_html=A