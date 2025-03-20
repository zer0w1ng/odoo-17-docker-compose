from odoo import api,fields,models,tools,SUPERUSER_ID
from odoo.exceptions import AccessError,UserError
from odoo.osv import expression
from odoo.tools import Query
from odoo.tools.translate import _
import json,logging
_logger=logging.getLogger(__name__)
class Applicant(models.Model):
	_inherit='hr.applicant';_order='ticket_number, priority desc, id desc';ticket_number=fields.Char(string='Ticket number',default='/',readonly=True,index=True);new_datetime=fields.Datetime('New Datetime');served_datetime=fields.Datetime('Served Datetime',index=True)
	def test_websocket(A):A._page_refresh_js()
	def _page_refresh_js(B):
		A=B.env.user.partner_id
		if A:B.env['bus.bus']._sendone(A,'page_refresh2',{'message':'Websocket Test'});_logger.debug('PAGE REFRESH %s',A.name)
	@api.model_create_multi
	def create(self,vals_list):
		B=vals_list
		for A in B:
			if A.get('ticket_number','/')=='/':A['ticket_number']=self._prepare_ticket_number_create(A);A['new_datetime']=fields.Datetime.now();A['served_datetime']=False
		self._page_refresh_js();return super().create(B)
	def write(B,vals):
		A=vals
		if A.get('stage_id'):
			C=B.env['hr.recruitment.stage'].browse(A.get('stage_id'))
			if C.name=='New':A['new_datetime']=fields.Datetime.now();A['served_datetime']=False;B._page_refresh_js()
			elif C.name=='Initial Qualification'and not A.get('served_datetime'):A['served_datetime']=fields.Datetime.now();B._page_refresh_js()
		return super().write(A)
	def _action_open_queue_display(A):return{'type':'ir.actions.act_url','target':'new','url':'/recruitment_queue'}
	def _action_open_kiosk(A):return{'type':'ir.actions.act_url','target':'new','url':'/recruitment_kiosk'}
	def acion_queue_applicant(A):A.ensure_one()
	def _prepare_ticket_number_create(C,values):
		B=values;A=C.env['ir.sequence']
		if'company_id'in B:A=A.with_company(B['company_id'])
		return A.next_by_code('ez_recruitment_queue.ticket.sequence')or'/'
	def _prepare_ticket_number(C,values):
		B=values;A=C.env['ir.sequence']
		if'company_id'in B:A=A.with_company(B['company_id'])
		return A.next_by_code('ez_recruitment_queue.ticket.sequence')or'/'
	def action_open_queue_controller(A):0
class QueueController(models.TransientModel):
	_name='ez.wiz.queue_controller';notification=fields.Char()
	def action_next_queue(A):B=A.env['hr.applicant'].search([('stage_id.name','=','New')],limit=1);return A._get_wizard(B,'Initial Qualification')
	def _get_wizard(A,applicant_id,to_stage):B=A.env['hr.recruitment.stage'].search([('name','=',to_stage)],limit=1);applicant_id.stage_id=B.id;C=A.env.context;D='ez.wiz.queue_controller';return{'name':_('Queue Controller'),'type':'ir.actions.act_window','view_type':'form','view_mode':'form','res_model':D,'target':'new','context':C}
	def action_previous_queue(A):B=A.env['hr.applicant'].search([('stage_id.name','=','Initial Qualification')],limit=1,order='ticket_number desc');return A._get_wizard(B,'New')
	def action_reset_queue(A):C=A.sudo().env.ref('ez_recruitment_queue.ir_sequence_ticket_number');C.number_next_actual=1;B=A.env['hr.applicant'].search([('stage_id.name','in',['New','Initial Qualification'])]);B.write({'active':False});B._page_refresh_js()