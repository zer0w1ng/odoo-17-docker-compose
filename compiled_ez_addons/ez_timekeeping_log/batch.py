from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp,logging
_logger=logging.getLogger(__name__)
class TimeCardBatch(models.TransientModel):
	_inherit='wz.timecard.batch'
	def batch_fill_time_logs(A):
		A.ensure_one()
		if not A.date1 or not A.date2 or A.date1>A.date2:raise ValidationError(_('Incomplete or wrong date range.'))
		B=A.env['ez.time.card'].search(['&',('company_id','=',A.env.user.company_id.id),'|','&',('date1','>=',A.date1),('date1','<=',A.date2),'&',('date2','>=',A.date1),('date2','<=',A.date2)]);_logger.debug('batch_fill_time_logs');B.fill_time_logs();B.summarize();return{'context':A.env.context,'view_type':'form','view_mode':'form','res_model':'wz.timecard.batch','res_id':A.id,'view_id':A.env.ref('ez_timekeeping.form_batch').id,'type':'ir.actions.act_window','target':'new'}