# -*- encoding: utf-8 -*-

import json
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class WizardDispersion(models.TransientModel):
    _name = 'wizard.dispersion'

    # hace falta agregar el id de empresa

    facturas = fields.Many2many('account.move',
                                domain=["&", "&", "&", ["pagar_factura", "=", True], ["state", "=", "posted"], "|",
                                        ["state", "=", "posted"], ["payment_state", "=", "not_paid"], "|", "&",
                                        ["payment_state", "=", "not_paid"], ["state", "=", "posted"], "&",
                                        ["payment_state", "=", "partial"], ["state", "=", "posted"]], required=True)

    # facturas = fields.Many2many('account.move', domain=[('pagar_factura', '=', True), ('state', '=', 'posted'),
    #                                                     ('move_type', '=', 'in_invoice')], required=True)

    reference = fields.Char(string="Referencia",
                            default=lambda self: self.env['ir.sequence'].next_by_code('dispersion.ref'), required=True)


    # @api.model
    # def _get_bank_account_domain(self):
    #     return [('id', 'in', self.env.user.company_id.partner_id.bank_ids.ids)]
    #
    # bank_account = fields.Many2one('res.partner.bank', string="Cuenta emisora del pago",
    #                                domain=_get_bank_account_domain, required=True)

#    bank_account = fields.Many2one('res.partner.bank', string="Cuenta emisora del pago",
#                                    domain= [('id', 'in', [2072, 2333])], required=True)

    bank_account = fields.Many2one('res.partner.bank', string="Cuenta emisora del pago",
                                    domain= [('cuenta_pagadora', '=', True)], required=True)

    def create_report(self):
        if not self.facturas:
            raise ValidationError(_('Se requieren facturas para procesar'))
        for factura in self.facturas:
            if not factura.partner_bank_id and not factura.partner_id.bank_ids:
                raise ValidationError(
                    _('La factura %s no tiene especificada una cuenta bancaria, necesaria para la dispersión.\nFavor '
                      'de especificar los datos requeridos en la factura y/o en la ficha del partner.' % (
                          factura.name)))
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary_text/dispersion?records=%s&reference=%s&account=%s' % (
                json.dumps(dict.fromkeys(self.facturas.ids, 1)), self.reference, self.bank_account.id),
            'target': 'main',

        }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
