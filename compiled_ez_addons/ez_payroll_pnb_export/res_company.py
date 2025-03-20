from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError,Warning
import logging
_logger=logging.getLogger(__name__)
class Company(models.Model):_inherit='res.company';pnb_branch_code=fields.Char('Branch Code');pnb_company_code=fields.Char('Company Code')