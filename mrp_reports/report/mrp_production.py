# -*- coding: utf-8 -*-

from odoo import api, models


class ReportMrpMaterials(models.AbstractModel):
    _name = 'report.mrp_reports.report_mrpmaterials'
    _description = 'Production Materials Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].browse(docids)
        moves = self.env['stock.move'].search([('raw_material_production_id', 'in', docids)])
        by_product = self.env['stock.move'].read_group(domain=[('raw_material_production_id', 'in', docids)],
                                                       fields=['product_uom:array_agg', 'product_uom_qty'],
                                                       groupby=['product_id'])
        for product in by_product:
            product['moves'] = moves.search([('id', 'in', moves.ids), ('product_id', '=', product['product_id'][0])])
        names = ['%s ' % doc.name for doc in docs]
        return {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'docs': docs[0],
            'names': names,
            'lines': by_product,
        }
