from openerp.osv import fields, osv

class tailor_records(osv.osv):

	_name = 'tailor.records'
	_rec_name = 'code'
	_columns = {
		'customer' : fields.many2one('res.partner','Customer',size=5,required='True'),
		'tailor':fields.many2one("res.users","Tailor", required=True),
		'product' : fields.many2one('product.template','Product',size=5,required='True'),
		'code' : fields.char('Order No.', readonly=True),
		'order_date' : fields.datetime('Order Date',size=5),
		'custom_shirts' : fields.integer('Custom Shirts(Pcs)',size=5),
		'monogram' : fields.integer('Monogram(Rs.)',size=5),
		'dealer' : fields.char('Dealer'),
		'promise_date' : fields.datetime('Promise Date',size=5),
		'shalwar_kameez' : fields.integer('Shalwar Kameez(Pcs.)',size=5),
		'over_size' : fields.integer('Over Size (Rs.)',size=5),
		'choose' : fields.selection([('dfa','DFA')],'Choose',size=5),
		'fitting' : fields.selection([('regular','Regualr Fit')],'Fitting'),
		'active' : fields.boolean('Active',size=5),
		'trousers' : fields.integer('Trouser/Pants(Pcs)',size=5),
		'neck' : fields.float('Neck'),
		'chest' : fields.float('Chest'),
		'waist' : fields.float('Waist'),
		'sleeve_left' : fields.float('Sleeve(Left)'),
		'sleeve_right' : fields.float('Sleeve(Right)'),
		'tail' : fields.float('Tail'),
		'hips' : fields.float('Hips/Seat'),
		'yoke' : fields.float('Yoke'),
		'wrist_right' : fields.float('Wrist(Right)'),
		'wrist_left' : fields.float('Wrist(Left)'),
		'neck_design' : fields.selection([('curve','Curve Point Classic')],'Neck Design'),
		'sleeve_design' : fields.selection([('square','Square Corner French')],'Sleeve Design'),
		'pocket_design' : fields.selection([('round','Round Cornered')],'Pocket Design'),
		'front_design' : fields.selection([('sport','Sport Front')],'Front Design'),
		}

	_defaults ={
	'active': 1,
	}

	def print_record(self, cr, uid, ids, context=None):

		assert len(ids) == 1, 'This option should only be used for a single id at a time'
		self.signal_workflow(cr, uid, ids, 'quotation_sent')
		return self.pool['report'].get_action(cr, uid, ids, 'Tailor.records_info_report', context=context)

	def create(self,cr,uid,vals,context=None):
		# if vals.get("code","/")=="/":
		vals["code"]=self.pool.get("ir.sequence").get(cr,uid,"tailor.records") or "/"
		return super(tailor_records,self).create(cr,uid,vals,context=context)
		
tailor_records()

class customer(osv.osv):
	_inherit = 'res.partner'

customer()
