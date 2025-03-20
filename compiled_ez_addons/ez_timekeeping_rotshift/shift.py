from odoo import api,fields,models,tools,_
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger=logging.getLogger(__name__)
DF='%Y-%m-%d'
class Shift(models.Model):
	_inherit='ez.shift'
	def get_rotate_start(B):A=fields.Date.from_string(fields.Date.context_today(B));C=A.weekday();A=A-relativedelta(days=C);return A
	is_rotate_shift=fields.Boolean('Rotating Shift');rotate_date_start=fields.Date('Date Start',default=get_rotate_start);rotate_ids=fields.One2many('ez.shift.rotate','shift_id','Rotate Schedule');invisible_sched=fields.Boolean(compute='_get_invisible_sched2')
	@api.depends('is_rotate_shift')
	def _get_invisible_sched2(self):
		for A in self:A.invisible_sched=A.is_rotate_shift
	@api.model
	def get_schedule(self,date1,date2):
		L=date2;K=date1;A=self;A.ensure_one()
		if A.is_rotate_shift:
			G={};C=fields.Date.from_string(K);Q=fields.Date.from_string(L);M=fields.Date.from_string(A.rotate_date_start);H={};B=0;F=0
			for N in A.rotate_ids:
				if len(N.line_shift_id.details)!=7:raise ValidationError(_('Schedule for rotating shifts must be of 7 days.\n%s - %s')%(A.name,line_shift_id.name))
				for I in N.line_shift_id.details:D='%s-%s'%(B,I.day);H[D]=I;_logger.debug('base schedule: k=%s day=%s',D,I.day);F+=1
				B+=1
			_logger.debug('schedule: %s',H);O=B
			if F==0:raise ValidationError(_('Invalid rotating shift definition.\n%s')%A.name)
			R=int(M.strftime('%w'));P=(10000*F+(C-M).days)%F;E=P%7;B=(P-E)/7%O
			while C<=Q:
				D='%s-%s'%(int(B),(E+R)%7);J=H.get(D);_logger.debug('schedule: k=%s date=%s day=%s dow=%s',D,C.strftime(DF),J and J.day,C.strftime('%w'));G[C.strftime(DF)]=J;C+=relativedelta(days=1);E+=1
				if E>=7:B=(B+1)%O;E=0
		else:G=super(Shift,A).get_schedule(K,L)
		return G
class RotateLines(models.Model):_name='ez.shift.rotate';_description='Rotating Shift Schedule';_order='sequence, id';shift_id=fields.Many2one('ez.shift','Shift',ondelete='cascade',readonly=True);sequence=fields.Integer('Seq',default=10);line_shift_id=fields.Many2one('ez.shift','Shift');name=fields.Char(related='line_shift_id.name',readonly=True);days=fields.Integer(default=7);note=fields.Text('Notes')