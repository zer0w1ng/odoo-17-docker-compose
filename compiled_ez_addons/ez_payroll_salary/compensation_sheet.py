from odoo import api,fields,models,tools,_
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,logging
_logger=logging.getLogger(__name__)
class WorkSummaryLine(models.Model):_inherit='ez.work.summary.line';campaign=fields.Char();salary_rate=fields.Float('Salary',digits='Payroll Amount');salary_rate_period=fields.Selection([('daily','per day'),('monthly','per month')],'Period')