from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'A visit by a patient to a doctor'

    name = fields.Char()
    visit_date = fields.Datetime()
    visit_stop_date = fields.Datetime()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    diagnosis_id = fields.Many2one(comodel_name='hr_hospital.diagnosis')
    recommendation = fields.Char()
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('canceled', 'Canceled')],
        default='planned')

    @api.ondelete(at_uninstall=False)
    def _unlink_without_diagnosis(self):
        for obj in self:
            if obj.diagnosis_id:
                raise UserError(_('It can not delete visit with diagnosis!'))
