from openerp.osv import fields, osv

class account_invoices(osv.osv):
	_inherit='account.invoice'
	_columns={
	'customer':fields.many2one('tailor.records','Customer',size=50),
		'code' : fields.integer('Order No.',size=5),
		'order_date' : fields.datetime('Order Date',size=5),
		'neck' : fields.float('Neck'),
		'chest' : fields.float('Chest'),
		'waist' : fields.float('Waist'),
		'sleeve_left' : fields.float('Sleeve(Left)'),
		'sleeve_right' : fields.float('Sleeve(Right)'),
		'tail' : fields.float('Tail'),
		'hips' : fields.float('Hips/Seat'),
		'yoke' : fields.float('Yoke'),
		'wrist_right' : fields.float('Wrist(Right)'),
		'wrist_left' : fields.float('Wrist(Left)')
	}

	def action_invoice_sent(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes ehapi closing '''
		action_dict = super(account_invoices, self).action_invoice_sent(cr, uid, ids, context=context)
		try:
			template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'Tailor', 'email_template_edi_invoice')[1]
			# assume context is still a dict, as prepared by super
			ctx = action_dict['context']
			ctx['default_template_id'] = template_id
			ctx['default_use_template'] = True
		except Exception:
			pass
		return action_dict

account_invoices()
