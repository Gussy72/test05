# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    factura_revisada = fields.Boolean(string="Factura Revisada")
    pagar_factura = fields.Boolean(string="Pagar Factura")
    fecha_programada_para_pago = fields.Date(string="Fecha Programada para Pago")

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
    dispersion_reference = fields.Char(string="Ref Dispersion", readonly=True)

    @api.model
    def create(self, values):
        if 'partner_id' in values:
            partner = self.env['res.partner'].browse((values['partner_id']))
            values['dispersion_type'] = partner.dispersion_type
            values['disponibilidad'] = partner.disponibilidad
            values['tipo_cuenta'] = partner.tipo_cuenta
            values['concepto_cie'] = partner.concepto_cie
            values['referencia_cie'] = partner.referencia_cie
            values['convenio_cie'] = partner.convenio_cie
        return super(AccountInvoice, self).create(values)

    @api.onchange('partner_id')
    def update_dispersion(self):
        self.dispersion_type = self.partner_id.dispersion_type
        self.disponibilidad = self.partner_id.disponibilidad
        self.tipo_cuenta = self.partner_id.tipo_cuenta
        self.concepto_cie = self.partner_id.concepto_cie
        self.referencia_cie = self.partner_id.referencia_cie
        self.convenio_cie = self.partner_id.convenio_cie
