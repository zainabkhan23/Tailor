{
    "name" : "Tailor",
	"version": "1.0",
	"author":"ehAPI Technologies LLC",
	"website":"http://www.ehapi.com",
	"category":"Tools",
	"depends":["base","sale","report","stock","stock_account"],
	# "depends":["base","board",'remove_taxes','mail','email_template',"report",'sale','stock','purchase'],

	"description":"Tailor module for ehAPI",

	"data": ["views/records_view.xml",
			 "views/sale_order_view.xml",
			 "views/products_view.xml",
			 "views/invoice_view.xml",
			 "views/inventory_view.xml",
			 "views/tailor_sequencing.xml",
			 "security/tailor_security_view.xml",
			 "security/ir.model.access.csv",
			 "reports/records_info.xml",
			 "reports/records_info_template.xml",
			 "reports/report_saleorder.xml",
			 "reports/report_invoice.xml",
			 "edi/invoice_saleorder_email.xml",
			 ],
			 
     
	"installable": True,

}