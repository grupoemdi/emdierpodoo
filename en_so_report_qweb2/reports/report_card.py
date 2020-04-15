from odoo import api, models


class ParticularReport(models.AbstractModel):
    _name = 'report.en_so_report_qweb2.report_so2'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("HOLA BEBOS")
        print("*******************************************")
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('module.report_name')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return docargs