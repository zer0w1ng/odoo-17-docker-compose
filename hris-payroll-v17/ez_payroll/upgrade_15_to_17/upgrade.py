from __future__ import print_function
import odoorpc,csv,re,random
from datetime import date
from pprint import pprint
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from string import ascii_lowercase
def get_external_id(odoo,model,id):
	A=odoo.env['ir.model.data'].search_read([('res_id','=',id),('model','=',model)],['complete_name'],limit=1)
	if A:return A[0]['complete_name']
	else:return False
def get_header(odoo,Object,has_message_fields=False):
	A=Object.fields_get();C=['id'];F=set(['one2many'])
	for D in sorted(A.keys()):
		E=A[D];B=True
		if E['type']in F:B=False
		if not has_message_fields and E['name'][:8]=='message_':B=False
		if B:C.append(D)
	return A,C
def create_employee(odoo1):A=odoo1;B=A.env['hr.department'];D,C=get_header(A,B);pprint(C)
def create_company(odoo):
	B=odoo.env.user.company_ids
	for A in B:print(A.name,get_external_id(odoo,'res.company',A.id))
if __name__=='__main__':odoo1=odoorpc.ODOO('ntt.ezpayrollweb.com',port=443,protocol='jsonrpc+ssl');user='admin';pwd='ebfeYUx2i5D2PZ6';db='ntt';odoo1.login(db,user,pwd);create_company(odoo1)