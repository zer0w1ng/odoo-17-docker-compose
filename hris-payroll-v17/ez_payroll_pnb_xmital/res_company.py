from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError,Warning
import logging
_logger=logging.getLogger(__name__)
class Company(models.Model):_inherit='res.company';pnb_branch_address=fields.Text('Branch / Address');pnb_signatory=fields.Char('Signatory');pnb_signatory_position=fields.Char('Position');pnb_account_name_number=fields.Char('Acct. Name / Number')