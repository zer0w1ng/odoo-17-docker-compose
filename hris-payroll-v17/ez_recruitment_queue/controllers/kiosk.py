from odoo.http import request,route,Controller,Response,content_disposition
from odoo import fields
import json,base64
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class HttpControllerKiosk(Controller):
	@route(['/rb_test'],type='http',auth='public',csrf=False)
	def test1(self):A=dict(request.params);_logger.debug('TEST: %s',A);return request.render('ez_recruitment_queue.test',{'fname':A.get('fname',''),'lname':A.get('lname','')})
	@route(['/rb_test2'],type='http',auth='public',csrf=False)
	def test2(self):A=dict(request.params);_logger.debug('TEST: %s',A);return request.render('ez_recruitment_queue.test',{})
	@route(['/recruitment_kiosk'],type='http',auth='public',csrf=False)
	def kiosk(self,**A):
		_logger.debug('KIOSK PARAM: kw=%s',A);E=A.get('selected_job_id')
		if E:B=request.env['hr.job'].browse(int(E));return request.render('ez_recruitment_queue.kiosk_applicant_entry',{'job_id':B})
		elif A.get('btn_submit'):
			id=A.get('job_id');B=request.env['hr.job'].browse(int(id));D=request.env['hr.applicant'].create({'name':B.name,'email_from':A.get('email_from'),'partner_mobile':A.get('partner_mobile'),'partner_name':A.get('partner_name'),'job_id':B.id});F=(fields.Datetime.from_string(D.create_date)+relativedelta(hours=8)).strftime('%m/%d/%Y %I:%M:%S %p');I=request.env['ir.config_parameter'].sudo().get_param('recruitment.print_data');G=json.loads(I)
			for C in G:
				if C['text']=='0001':C['text']=D.ticket_number
				if C['text']=='01/01/2024 12:00:00 PM':C['text']=F
			H=json.dumps(G);_logger.debug('CREATE: %s kw=%s print=%s',B,A,H);return request.render('ez_recruitment_queue.kiosk_printing',{'ticket_number':D.ticket_number,'print_data':H,'dt':F})
		else:return self.open_kiosk_start_page()
	def open_kiosk_start_page(B):A=request.env['hr.job'].search([('website_published','=',True)]);return request.render('ez_recruitment_queue.kiosk_main_applicants',{'jobs':A})
	@route(['/recruitment_kiosk/apply/<int:job_id>'],type='http',auth='public',csrf=False)
	def kiosk_apply(self,job_id):
		B=job_id;A=dict(request.params);_logger.debug('APPLY: %s kw=%s',B,A);C=request.env['hr.job'].browse(B)
		if A.get('id_cancel'):return self.open_kiosk_start_page()
		elif A.get('id_submit')=='1':_logger.debug('CREATE: %s kw=%s',B,A);return request.render('ez_recruitment_queue.portal_apply_kiosk',{'job_rec':C,'submitted':True})
		else:return request.render('ez_recruitment_queue.portal_apply_kiosk',{'job_rec':C,'submitted':False})