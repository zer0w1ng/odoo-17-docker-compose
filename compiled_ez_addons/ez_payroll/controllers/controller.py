from collections import OrderedDict
from operator import itemgetter
from odoo import _,http
from odoo.osv import expression
from odoo.exceptions import AccessError,MissingError
from odoo.http import request
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal,pager as portal_pager
import logging
_logger=logging.getLogger(__name__)
class CustomerPortalHelpdesk(CustomerPortal):
	def _prepare_home_portal_values(C,counters):
		B=counters;A=super()._prepare_home_portal_values(B)
		if'payslip_count'in B:D=request.env['hr.ph.payslip'].sudo();E=D.search_count(C._get_payslip_domain(),limit=1);A['payslip_count']=E
		_logger.debug('COUNTERS: %s',A);return A
	def _payslip_get_page_view_values(B,payslip,access_token,**C):A=payslip;D={'page_name':'payslip','payslip':A};return B._get_page_view_values(A,access_token,D,'my_payslips_history',False,**C)
	def _get_payslip_domain(B):A=[('company_id','=',request.env.company.id),('employee_id.work_email','=',request.env.user.login),('state','!=','draft')];return A
	def _get_payslip_searchbar_sortings(A):return{'date_to':{'label':_('Date'),'order':'date_to desc'},'net_pay':{'label':_('Net Pay'),'order':'net_pay'},'deduction':{'label':_('Deductions'),'order':'total_deductions'}}
	def _get_payslip_searchbar_filters(A):return{'all':{'label':_('All'),'domain':[]}}
	@http.route(['/my/payslips','/my/payslips/page/<int:page>'],type='http',auth='user',website=True)
	def portal_my_payslips(self,page=1,date_begin=None,date_end=None,sortby=None,filterby=None,**D):A=self._prepare_my_payslips_values(page,date_begin,date_end,sortby,filterby);B=portal_pager(**A['pager']);_logger.debug('PAGER: %s',B);C=A['payslips'](B['offset']);request.session['my_payslips_history']=C.ids[:100];A.update({'payslips':C,'pager':B});return request.render('ez_payroll.portal_my_payslips',A)
	def _prepare_my_payslips_values(A,page,date_begin,date_end,sortby,filterby,domain=None,url='/my/payslips'):
		G=date_end;F=filterby;E=date_begin;C=sortby;B=domain;_logger.debug('PREPAGE: %s',page);H=A._prepare_portal_layout_values();D=request.env['hr.ph.payslip'].sudo();B=expression.AND([B or[],A._get_payslip_domain()]);I=A._get_payslip_searchbar_sortings()
		if not C:C='date_to'
		K=I[C]['order'];J=A._get_payslip_searchbar_filters()
		if not F:F='all'
		B+=J[F]['domain']
		if E and G:B+=[('date_to','>=',E),('date_to','<=',G)]
		H.update({'date':E,'payslips':lambda pager_offset:D.search(B,order=K,limit=A._items_per_page,offset=pager_offset)if D.check_access_rights('read',raise_exception=False)else D,'page_name':'payslip','pager':{'url':url,'url_args':{'date_begin':E,'date_end':G,'sortby':C},'total':D.search_count(B)if D.check_access_rights('read',raise_exception=False)else 0,'page':page,'step':A._items_per_page},'default_url':url,'searchbar_sortings':I,'sortby':C,'searchbar_filters':OrderedDict(sorted(J.items())),'filterby':F});return H
	@http.route(['/my/payslips/pdf/<int:payslip_id>'],type='http',auth='user',website=True)
	def portal_my_payslip_pdf_detail(self,payslip_id,**E):
		B=request.env['hr.ph.payslip'].sudo();A=B.browse(payslip_id)
		if A.employee_id.work_email!=request.env.user.login:return request.redirect('/my')
		C='pdf';D=False;return self._show_report(model=A,report_type=C,report_ref='ez_payroll.action_print_single_payslip',download=D)