# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import tempfile

from odoo import http
from odoo.http import request


class DispersionReport(http.Controller):

    @http.route(['''/web/binary_text/dispersion''', ], type='http', auth="user", csfr=False)
    def download_dispersion(self, records=False, reference=False, account=False, **post):
        if records and account:
            records = json.loads(records)
            reference = reference or '1234567'
            cuenta_ordenante = request.env['res.partner.bank'].sudo().browse(int(account)).acc_number.rjust(18, '0')
            ids = [int(key) for key in records.keys()]
            fp = tempfile.TemporaryFile()
            facturas = request.env['account.move'].sudo().browse(ids)

            for factura in facturas:
                if factura.dispersion_type in ['TSC', 'PSC'] and cuenta_ordenante:
                    cuenta_beneficiario = factura.partner_bank_id.acc_number
                    tipo_cuenta = factura.tipo_cuenta or '40'
                    if tipo_cuenta == '40':
                        cuenta_beneficiario = factura.partner_bank_id.l10n_mx_edi_clabe or ''
                    row = "%s%s%sMXP%016.2f%s%s%sPAGO DE %s%s%s\n" % (
                        factura.dispersion_type,
                        cuenta_beneficiario[:18].rjust(18, '0'),
                        cuenta_ordenante,
                        factura.amount_residual,
                        factura.partner_id.name[:30].ljust(30),
                        tipo_cuenta,
                        factura.partner_bank_id.bank_id.l10n_mx_edi_code and factura.partner_bank_id.bank_id.l10n_mx_edi_code[
                                                                             :3] or factura.partner_bank_id.bank_id.bic and factura.partner_bank_id.bank_id.bic[
                                                                                                                            :3] or '000',
                        factura.name[:22].ljust(22),
                        reference[:7].rjust(7),
                        factura.disponibilidad,
                    )
                    fp.write(row.encode('utf-8'))
                    factura.write({'dispersion_reference': reference})
                cuenta_beneficiario = factura.partner_bank_id and factura.partner_bank_id.acc_number
                if not factura.partner_bank_id:
                    cuenta_beneficiario = factura.partner_id.bank_ids and factura.partner_id.bank_ids[
                        0].acc_number or ''
                if factura.dispersion_type in ['TNN', 'PTC'] and cuenta_ordenante:
                    row = "%s%s%s%s%016.2fPAGO DE %s\n" % (
                        factura.dispersion_type,
                        cuenta_beneficiario[:18].rjust(18, '0'),
                        cuenta_ordenante,
                        factura.currency_id.name == 'MXN' and 'MXP' or factura.currency_id.name,
                        factura.amount_residual,
                        factura.name[:22].ljust(22),
                    )
                    fp.write(row.encode('utf-8'))
                    factura.write({'dispersion_reference': reference})
                if factura.dispersion_type in ['CIL'] and cuenta_ordenante:
                    row = "%s%s%s%s%016.2fPAGO DE %s%s\n" % (
                        factura.dispersion_type,
                        factura.concepto_cie[:30].ljust(30),
                        factura.convenio_cie[:7].ljust(7),
                        cuenta_ordenante,
                        factura.amount_residual,
                        factura.name[:22].ljust(22),
                        factura.referencia_cie[:20].ljust(20),
                    )

                    fp.write(row.encode('utf-8'))
                    factura.write({'dispersion_reference': reference})
            fp.seek(0)
            file_data = fp.read()
            fp.close()
            return request.make_response(
                file_data, headers=[
                    ('Content-Disposition', 'attachment; filename="dispersion_pagos_ref_%s.TXT"' % (reference)),
                    ('Content-Type', 'text/plain')
                ]

            )
