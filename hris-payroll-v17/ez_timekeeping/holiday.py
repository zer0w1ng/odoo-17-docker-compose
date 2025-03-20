from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
import datetime
class Holidays(models.Model):
	_name='ez.holiday';_description='Holidays';_order='year desc, date desc';name=fields.Char('Name',required=True);year=fields.Char(required=True);date=fields.Date('Date');type=fields.Selection([('lh','Regular Holiday'),('sh','Special Holiday')],'Type',required=True,default=lambda self:'sh');note=fields.Text('Notes')
	@api.model
	def get_holidays(self):return[["New Year's Day",'01-01','lh'],['Maundy Thursday',None,'lh'],['Good Friday',None,'lh'],['Araw ng Kagitingan','04-09','lh'],['Labor Day','05-01','lh'],['Independence Day','06-12','lh'],['National Heroes Day',None,'lh'],['Bonifacio Day','11-30','lh'],['Christmas Day','12-25','lh'],['Rizal Day','12-30','lh'],['Chinese New Year',None,'sh'],['Black Saturday',None,'sh'],['Ninoy Aquino Day','08-21','sh'],['All Saints Day','11-01','sh'],['Last Day of the Year','12-31','sh']]
	@api.model
	def create_holiday_year(self,year):
		E=self;A=year
		for C in E.get_holidays():
			F=C[0]
			if C[1]:D='%s-%s'%(A,C[1])
			else:D=None
			H=C[2];I=E.search([('name','=',F),('year','=',A)])
			try:G=int(A)
			except:G=0
			if G>2000 and not I:
				if not D:
					if F=='National Heroes Day':
						B=datetime.date(year=int(A),month=8,day=20)
						while B.month==8:
							if B.weekday()==0:D=B.strftime('%Y-%m-%d')
							B=B+datetime.timedelta(days=1)
				E.create({'name':F,'type':H,'date':D,'year':A})
class CreateHolidays(models.TransientModel):
	_name='ez.create.holiday.wizard';_description='Create Holidays Wizard';year=fields.Char('Year',required=True,default=lambda self:datetime.datetime.now().year)
	def create_holidays(A):A.ensure_one();A.env['ez.holiday'].create_holiday_year(A.year);return{'name':_('Holidays'),'view_type':'form','view_mode':'tree,calendar','res_model':'ez.holiday','view_id':False,'type':'ir.actions.act_window','domain':[('year','=',A.year)]}