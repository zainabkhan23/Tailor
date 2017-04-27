from openerp.osv import fields, osv
from openerp import api

class sale_order(osv.osv):

	_inherit="sale.order"
	_columns = {
		'customer':fields.many2one('tailor.records','Customer',size=50),
		'tailor':fields.many2one("res.users","Tailor", required=True),
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

	def onchange_partner_id(self, cr, uid, ids, part, context=None):

		print 'my onchange'

		if not part:
			return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False,  'payment_term': False, 'fiscal_position': False}}
		part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
		addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])
		pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
		payment_term = part.property_payment_term and part.property_payment_term.id or False
		dedicated_salesman = part.user_id and part.user_id.id or uid
		val = {
			'partner_invoice_id': addr['invoice'],
			'partner_shipping_id': addr['delivery'],
			'payment_term': payment_term,
			'user_id': dedicated_salesman,
		}
		delivery_onchange = self.onchange_delivery_id(cr, uid, ids, False, part.id, addr['delivery'], False,  context=context)
		val.update(delivery_onchange['value'])

		# Getting Measurements of customer
		measurement_ids = self.pool.get('tailor.records').search(cr, uid, [('customer', '=', part.id)])
		if measurement_ids:
			# create browse object thing
			meare_obj = self.pool.get('tailor.records').browse(cr, uid, measurement_ids[0])
			val['neck'] = meare_obj.neck
			val['chest'] = meare_obj.chest
			val['waist'] = meare_obj.waist
			val['sleeve_left'] = meare_obj.sleeve_left
			val['sleeve_right'] = meare_obj.sleeve_right
			val['tail'] = meare_obj.tail
			val['hips'] = meare_obj.hips
			val['yoke'] = meare_obj.yoke
			val['wrist_left'] = meare_obj.wrist_left
			val['wrist_right'] = meare_obj.wrist_right
		if pricelist:
			val['pricelist_id'] = pricelist
		sale_note = self.get_salenote(cr, uid, ids, part.id, context=context)
		if sale_note: val.update({'note': sale_note})  
		return {'value': val}


	def action_quotation_send(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes a ehapi closing and additional table '''
		action_dict = super(sale_order, self).action_quotation_send(cr, uid, ids, context=context)
		try:
			template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'Tailor', 'email_template_edi_sale')[1]
			# assume context is still a dict, as prepared by super
			ctx = action_dict['context']
			ctx['default_template_id'] = template_id
			ctx['default_use_template'] = True
		except Exception:
			pass
		return action_dict	
	   
	

# override the function to create invoice with the custom field values
	def _prepare_invoice(self, cr, uid, order, lines, context=None):
		if context is None:
			context = {}
		journal_ids = self.pool.get('account.journal').search(cr, uid,
			[('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
			limit=1)
		if not journal_ids:
			raise osv.except_osv(_('Error!'),
				_('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
		invoice_vals = {
			'name': order.client_order_ref or '',
			'origin': order.name,
			'type': 'out_invoice',
			'reference': order.client_order_ref or order.name,
			'account_id': order.partner_id.property_account_receivable.id,
			'partner_id': order.partner_invoice_id.id,
			'journal_id': journal_ids[0],
			'invoice_line': [(6, 0, lines)],
			'currency_id': order.pricelist_id.currency_id.id,
			'comment': order.note,
			'payment_term': order.payment_term and order.payment_term.id or False,
			'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
			'date_invoice': context.get('date_invoice', False),
			'company_id': order.company_id.id,
			'user_id': order.user_id and order.user_id.id or False,
			'section_id' : order.section_id.id,
			'neck' : order.neck,
			'chest' : order.chest,
			'waist' : order.waist,
			'sleeve_left' : order.sleeve_left,
			'sleeve_right' : order.sleeve_right,
			'tail' : order.tail,
			'hips' : order.hips,
			'yoke' : order.yoke,
			'wrist_right' : order.wrist_right,
			'wrist_left' : order.wrist_left,
			}
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals


	# def action_quotation_send(self, cr, uid, ids, context=None):
	# 	'''  Override to use a modified template that includes a ehapi closing and additional table '''
	# 	action_dict = super(sale_order, self).action_quotation_send(cr, uid, ids, context=context)
	# 	try:
	# 		template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'Tailor', 'email_template_edi_sale')[1]
	# 		# assume context is still a dict, as prepared by super
	# 		ctx = action_dict['context']
	# 		ctx['default_template_id'] = template_id
	# 		ctx['default_use_template'] = True
	# 	except Exception:
	# 		pass
	# 	return action_dict



sale_order()
