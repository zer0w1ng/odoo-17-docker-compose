from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError,Warning
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from odoo.tools.misc import xlwt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,base64
from io import BytesIO
import logging
_logger=logging.getLogger(__name__)
class Payroll(models.Model):
	_inherit='hr.ph.payroll';pnb_company_code=fields.Char(compute='_get_pnb_code');pnb_branch_code=fields.Char(compute='_get_pnb_code');pnb_posting_date=fields.Date('Posting Date',default=fields.Date.context_today);pnb_excel_file=fields.Binary('FastBuck Excel',readonly=True);pnb_filename=fields.Char(readonly=True);pnb_ups_file=fields.Binary('FastBuck UPS File',readonly=True);pnb_ups_filename=fields.Char(readonly=True)
	@api.depends('company_id')
	def _get_pnb_code(self):
		A=self
		for B in A:C=A.company_id.pnb_company_code or'';D=A.company_id.pnb_branch_code or'';B.pnb_company_code=C.strip()[:5].zfill(5);B.pnb_branch_code=D.strip()[:4].zfill(4)
	def create_pnb_excel_file(B):
		B.ensure_one();H=xlwt.Workbook();E=H.add_sheet('Sheet1');D=0
		for C in B.payslip:
			if C.net_pay>.0:
				I=C.employee_id.atm_no;J=C.employee_id.last_name;K=C.employee_id.first_name
				if I:E.write(D,0,I)
				if J:E.write(D,1,J)
				if K:E.write(D,2,K)
				E.write(D,3,C.net_pay);D+=1
		L=BytesIO();H.save(L);F=base64.b64encode(L.getvalue());B.pnb_excel_file=F;M=fields.Date.from_string(B.pnb_posting_date);B.pnb_filename='payroll-pnb-%s.xls'%M.strftime('%m%d%Y');A='';N=0;O=0;G=M.strftime('%m%d%y')
		for C in B.payslip:
			if C.net_pay>.0:P=int(round(C.net_pay*100));N+=P;A+='052';A+=B.pnb_branch_code;A+=B.pnb_company_code;A+=G;A+=('%d'%P).zfill(12);Q=(C.employee_id.atm_no or'')[:16].zfill(16);A+=Q;A+=(C.employee_id.last_name or'').ljust(20)[:20];A+=(C.employee_id.first_name or'').ljust(20)[:20];A+='\r\n';O+=1
		A+='099';A+=B.pnb_branch_code;A+=B.pnb_company_code;A+=G;A+=('%d'%N).zfill(12);A+=('%d'%O).zfill(10);A+='\r\n';R=A.encode('ascii','replace');F=base64.b64encode(R);B.pnb_ups_file=F;B.pnb_ups_filename='PAY%s_%s.UPS'%(B.pnb_company_code,G)