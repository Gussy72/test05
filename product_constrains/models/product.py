# -*- coding: utf-8 -*-
import odoo
from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'


    _sql_constraints = [
        ('barcode_uniq', 'Check(1=1)', "A barcode can only be assigned to one product !"),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
