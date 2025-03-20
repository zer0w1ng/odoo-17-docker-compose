from odoo.http import request,route,Controller,Response,content_disposition
from odoo import fields
import json,base64
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class HttpController(Controller):
	@route(['/test_owl'],type='http',auth='public')
	def show_playground(self):A,B,C,D=self._get_queue();return request.render('ez_recruitment_queue.recruitment_queue_websocket',{'nl_items':A,'ns_items':B,'now_serving':C,'wait':'%s'%timedelta(seconds=int(D))})
	@route(['/recruitment_queue/<string:process>/<int:applicant_id>'],type='http',auth='user',cors='*')
	def queue_process(self,process,applicant_id,**J):
		B=int(applicant_id)
		if process=='next':A='Initial Qualification'
		else:A='New'
		C=request.env['hr.recruitment.stage'].search([('name','=',A)],limit=1);D=request.env['hr.applicant'].browse(B);D.stage_id=C
		if 1:return request.redirect('/recruitment_queue')
		else:E,F,G,H=self._get_queue();I=request.env.company;return request.render('ez_recruitment_queue.recruitment_queue_websocket',{'nl_items':E,'ns_items':F,'now_serving':G,'company':I,'wait':'%s'%timedelta(seconds=int(H))})
	def _get_queue(R):
		O=request.env['hr.applicant'].sudo().search([('ticket_number','!=','/'),('stage_id.name','=','New')],limit=16);F=request.env['hr.applicant'].sudo().search([('ticket_number','!=','/'),('stage_id.name','!=','New')],limit=5,order='served_datetime desc');E=[A for A in O]
		if len(E)<16:
			D=16-len(E)
			for P in range(D):E.append(False)
		H=[];A=0
		for L in range(4):
			H.append([])
			for Q in range(4):
				if E[A]:C='/recruitment_queue/next/%s'%E[A].id
				else:C='/recruitment_queue'
				H[L].append([E[A],C]);A+=1
		I=.0;J=0
		if F:
			for G in F:
				if G.served_datetime and G.new_datetime:M=fields.Datetime.from_string(G.served_datetime);N=fields.Datetime.from_string(G.new_datetime);I+=(M-N).seconds;J+=1;_logger.debug('WAIT: %s %s serv=%s new=%s wait=%s',G.ticket_number,J,M,N,I)
			if J:I/=J
		B=[A for A in F if A.stage_id.name=='Initial Qualification']
		if len(B)<5:
			D=5-len(B)
			for P in range(D):B.append(False)
		K=[];A=1
		if B[0]:C='/recruitment_queue/back/%s'%B[0].id
		else:C='/recruitment_queue'
		F=[B[0],C]
		for L in range(2):
			K.append([])
			for Q in range(2):
				if B[A]:C='/recruitment_queue/back/%s'%B[A].id
				else:C='/recruitment_queue'
				K[L].append([B[A],C]);A+=1
		for D in H:_logger.debug('NEXT IN LINE: %s',D)
		for D in K:_logger.debug('NOW SERVING: %s',D)
		return H,K,F,I
	@route(['/recruitment_queue'],type='http',auth='user',cors='*')
	def queue(self,applicant_id=False,**F):A,B,C,D=self._get_queue();E=request.env.company;return request.render('ez_recruitment_queue.recruitment_queue_websocket',{'nl_items':A,'ns_items':B,'now_serving':C,'company':E,'wait':'%s'%timedelta(seconds=int(D))})