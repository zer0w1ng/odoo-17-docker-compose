from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class PayslipDeductionReport(models.Model):
	_name='hr.ph.pay.deduction.report';_description='Deduction Report';_auto=False;company_id=fields.Many2one('res.company',string='Company',readonly=True);year=fields.Char(readonly=True);year_month=fields.Char(readonly=True);employee_id=fields.Many2one('hr.employee',string='Employee',readonly=True);gross_pay=fields.Float('Gross',digits=(12,2),readonly=True);basic_pay=fields.Float('Basic',digits=(12,2),readonly=True);taxable=fields.Float('Taxable',digits=(12,2),readonly=True);sss_ee=fields.Float('SSS EE',digits=(12,2),readonly=True);sss_er=fields.Float('SSS ER',digits=(12,2),readonly=True);hdmf_ee=fields.Float('HDMF EE',digits=(12,2),readonly=True);hdmf_er=fields.Float('HDMF ER',digits=(12,2),readonly=True);phic_ee=fields.Float('PHIC EE',digits=(12,2),readonly=True);phic_ee=fields.Float('PHIC ER',digits=(12,2),readonly=True);wtax=fields.Float('WTAX',digits=(12,2),readonly=True)
	def init(A):tools.drop_view_if_exists(A._cr,'hr_ph_pay_deduction_report');A._cr.execute('\n            CREATE VIEW hr_ph_pay_deduction_report AS (\n                SELECT MIN(id) AS id,\n                    company_id,\n                    left(year_month, 4) AS year,\n                    year_month,\n                    employee_id,\n                    SUM(gross_pay) as gross_pay,\n                    SUM(basic_pay) as basic_pay,\n                    SUM(taxable) as taxable\n                FROM hr_ph_pay_deduction\n                GROUP BY company_id, year_month, employee_id\n\n            )')