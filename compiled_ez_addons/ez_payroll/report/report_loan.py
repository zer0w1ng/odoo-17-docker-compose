from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
class ReportLoan(models.Model):_name='ez.loan.report';_description='Loan Payment Report';_auto=False