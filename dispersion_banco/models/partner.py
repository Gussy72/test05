# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_cuenta = fields.Selection([('40', 'Cuenta Clabe'),
                                    ('03', 'Tarjeta de Débito'),
                                    ], string='Tipo de Cuenta', default="40")
    disponibilidad = fields.Selection([('H', 'Mismo día vía SPEI'),
                                       ('M', 'Día siguiente vía CECOBAN'),
                                       ], string='Disponibilidad', default="H")
    dispersion_type = fields.Selection([('TSC', 'Traspaso Interbancario'),
                                        ('TNN', 'Traspaso Bancomer'),
                                        ('PTC', 'Pago Bancomer'),
                                        ('PSC', 'Pago Interbancario'),
                                        ('OPI', 'Pago Internacional'),
                                        ('CIL', 'Pago a convenio CIE')
                                        ],
                                       string="Dispersion Type", default="PSC")
    concepto_cie = fields.Char(string="Concepto CIE", size=30)
    convenio_cie = fields.Char(string="Convenio CIE", size=7)
    referencia_cie = fields.Char(string="Referencia CIE", size=20)
