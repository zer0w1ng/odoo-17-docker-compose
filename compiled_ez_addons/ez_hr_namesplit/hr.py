from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from.import random_names
import random
_logger=logging.getLogger(__name__)
class ResourceResource(models.Model):_inherit='resource.resource';name=fields.Char(required=False)
def get_name(last_name,first_name,middle_name):
	C=middle_name;B=first_name;A=last_name
	if C:return'%s, %s %s'%((A or'Blank').strip(),(B or'').strip(),(C or'').strip())
	else:return'%s, %s'%((A or'Blank').strip(),(B or'').strip())
class HrEmployee(models.Model):
	_inherit='hr.employee';name=fields.Char(compute='_get_name',store=True);last_name=fields.Char('Last Name');first_name=fields.Char('First Name');middle_name=fields.Char('Middle Name')
	@api.depends('last_name','first_name','middle_name')
	def _get_name(self):
		for A in self:A.name=get_name(A.last_name,A.first_name,A.middle_name)
	@api.onchange('last_name','first_name','middle_name')
	def change_name(self):A=self;B=get_name(A.last_name,A.first_name,A.middle_name);A.name=B;_logger.debug('Change name: %s',B)
	def update_name(B):
		for A in B:C=get_name(A.last_name,A.first_name,A.middle_name);A.name=C
	def write(C,vals):
		B=vals
		def E(vals):
			A=['last_name','first_name','middle_name']
			for B in A:
				if B in vals:return True
			return False
		F=super(HrEmployee,C).write(B)
		if E(B)or B.get('name'):
			for A in C:
				D=get_name(A.last_name,A.first_name,A.middle_name)
				if D!=A.name:A.write({'name':D})
		return F
	@api.model_create_multi
	def create(self,vals_list):
		B=vals_list
		for A in B:A.update({'name':get_name(A.get('last_name'),A.get('first_name'),A.get('middle_name'))})
		return super().create(B)
	@api.model
	def demo_namesplit(self):
		A=self.search([])
		for B in A:C,D,E=random_names.get_random_name();B.write({'last_name':C,'first_name':D,'middle_name':E})
	@api.model
	def demo_create_employee(self,year):
		B=['id','last_name','first_name','middle_name','identification_id','tin_no','sss_no','phic_no','pagibig_no','atm_no','hired'];A=[]
		for C in range(20):D,E,F=random_names.get_random_name();G='ID-%05d'%random.randint(1,99999);H='-'.join(['%03d'%random.randint(100,999)for A in range(3)]);I='08-%07d-5'%random.randint(5000,9999999);J='15-%09d-5'%random.randint(5000,999999999);K='-'.join(['%04d'%random.randint(100,999)for A in range(3)]);L='-'.join(['%04d'%random.randint(100,999)for A in range(2)])+'-%02d'%random.randint(1,99);M='%s-01-01'%year;A.append(['__demo__.employee_%d'%C,D,E,F,G,H,I,J,K,L,M])
		N=self.env['hr.employee'].load(B,A);return N
class HrEmployeePublic(models.Model):_inherit='hr.employee.public';last_name=fields.Char();first_name=fields.Char();middle_name=fields.Char()